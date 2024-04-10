import React, { useState, useEffect, useCallback } from 'react';
import { publicDir } from "../../constants";
import Page from '../../components/layout/Page';
import styles from './ProfilePage.module.css';
import { useParams } from 'react-router-dom';
import { apiGetAuthor } from '../../api/authors';
import { getUserId } from '../../utils/auth';
import { apiDeleteFollower, apiInboxFollowRequest, apiGetFollower, apiGetFollowRequest} from '../../api/following';
import PostStream, { PostStreamTy } from '../../components/post/PostStream';
import { Col, Row } from 'react-bootstrap';
import SubscriptionCheckmark from '../../components/subscription/Checkmark';
import { toast } from 'react-toastify';

enum FollowState {
    FOLLOWING="following",
    PENDING="pending",
    NOT_FOLLOWING="not_following"
};

const ProfilePage: React.FC = () => {
    // GET request on user to request actual API?...
    const [authorId, setAuthorId] = useState<string>("");
    const [avatarURL, setAvatarURL] = useState(`${publicDir}/static/default-avatar.png`);
    const [githubUsername, setGithubUsername] = useState("");
    const [username, setUsername] = useState("");
    const [bio, setBio] = useState("");
    const [postCount, setPostCount] = useState(-1);
    const [followingCount, setFollowingCount] = useState(-1);
    const [followerCount, setFollowerCount] = useState(-1);
    const [followState, setFollowState] = useState<FollowState>(FollowState.NOT_FOLLOWING)
    const [subdomain, setSubdomain] = useState("");
    const [subscribed, setSubscribed] = useState(false);
    const [blocked, setBlocked] = useState(false);

    const loggedInAuthorId : string = getUserId()!; 
    const params = useParams();
    const userId = params["id"]!;

    /** Function to update the user's following */
    const updateFollowingState = useCallback(async (userId: string) => {
        const followRequestRes = await apiGetFollowRequest(loggedInAuthorId, userId);
        apiGetFollower(userId, loggedInAuthorId)
            .then(async response => {
                if (response.status !== 404) { 
                    setFollowState(FollowState.FOLLOWING);
                } else {
                    if (followRequestRes.status === 404) {
                        setFollowState(FollowState.NOT_FOLLOWING);
                    } else {
                        setFollowState(FollowState.PENDING);
                    }
                } 
            });
    }, [loggedInAuthorId]);

    /** Gets user profile */
    useEffect(() => {

        console.log("PUIBLIC URL:", process.env.PUBLIC_URL);

        apiGetAuthor(userId)
            .then(async author => {
                if (!author) {
                    console.error(`Failed to load user profile: ${userId}`);
                    return;
                }

                setUsername(author.displayName);
                setPostCount(author.posts);
                setFollowerCount(author.followers);
                setFollowingCount(author.following);
                setAuthorId(author.id);
                setBio(author.bio);
                setSubscribed(author.subscribed);
                setBlocked(!!author.blocked);

                if (author.github) {
                    setGithubUsername(author.github.substring("https://github.com/".length));
                }
                if (author.profileImage) {
                    setAvatarURL(author.profileImage);
                }

                let subdomain = author.host.split(".")[0];
                if (subdomain.indexOf("//") === -1) {
                    subdomain = "Invalid Origin URL";
                } else {
                    subdomain = subdomain.substring(subdomain.indexOf("//") + 2);
                }
                setSubdomain(subdomain);
            });
        
        if (userId) { 
            updateFollowingState(userId);
        }
         
    }, [params, updateFollowingState, userId]);

    /** Function to render the follow button based on following state */
    const renderFollowButton = () => {
        // Check that the user's profile is not the current user's
        if (userId === loggedInAuthorId) {
            return;
        }

        switch (followState) {
            // Show unfollow button if already following this user
            case FollowState.FOLLOWING:
                return (
                    <button className="btn btn-danger" onClick={async () => {
                        await apiDeleteFollower(authorId, loggedInAuthorId)
                            .then(status => {
                                if (status && status === 204) {
                                    setFollowerCount(followerCount - 1);
                                    setFollowState(FollowState.NOT_FOLLOWING);
                                }
                            });
                    }}>
                        Unfollow
                    </button>
                );
 
            case FollowState.PENDING:
                return (
                    <button className="btn btn-warning" onClick={() => {
                        toast.warning("Follow Request Already Pending!");
                    }}>
                        Pending
                    </button>
                );

            // Show follow button if not following
            case FollowState.NOT_FOLLOWING:
                return (
                    <button className="btn btn-primary" onClick={async () => {
                        const followRequestRes = await apiInboxFollowRequest(loggedInAuthorId, authorId); 
                        if (followRequestRes === null || followRequestRes.error) {
                            toast.error(`Failed to connect to remote host`);
                        } else { 
                            await updateFollowingState(authorId);
                            toast.success(`Follow Request Sent!`);
                        }
                    }}>
                        Follow
                    </button>
                );
        }
    };

    const renderBlockButton = () => {
        if (!userId) {
            return;
        }

        if (subscribed) {
            return <button className="btn btn-secondary block-btn">
                {blocked ? "Unblock" : "Block"}
            </button>;
        } else {
            return <button className="btn btn-secondary block-btn" disabled>
                {blocked ? "Unblock" : "Block"}
            </button>;
        }
    };
    
    /** Profile page */
    return <Page selected="Profile">
        <div id={styles.container}>
            <div id={styles.header}>
                {/** Github */}
                <div id={styles.github}>
                    {githubUsername ? (
                        <a href={`https://github.com/${githubUsername}`}>
                            <img alt="Github Account" src={`${publicDir}/static/github.png`} />
                        </a>
                    ) : null}
                </div>
                {/** Avatar and follow button */}
                <Row className={"align-items-end"}>
                    <Col id={styles.avatarContainer}>
                        <img alt="Profile Avatar" src={avatarURL} />
                    </Col>
                    <Col id={styles.profileButtons}>
                        {renderFollowButton()}
                        {renderBlockButton()}
                    </Col>
                </Row>
                {/** About the user */}
                <div id={styles.identityContainer}>
                    <h1 id={styles.username}>
                        {username}
                        {
                            subscribed ?
                                <div style={{
                                    display: "inline-block",
                                    height: 32,
                                    width: 32,
                                    marginLeft: 10,
                                    marginRight: 10
                                }}>
                                    <SubscriptionCheckmark />
                                </div>
                            : null
                        }
                        <span id={styles.subdomain}> {subdomain}</span>
                    </h1>
                    <h5 id={styles.bio}>{bio}</h5>
                </div>
                {/** Post statistics */}
                <Row id={styles.stats}>
                    <Col className={styles.item}>
                        <div>
                            <div>Posts</div>
                            <div className={styles.itemAmount}>{postCount === -1 ? "" : postCount}</div>
                        </div>
                    </Col>
                    <Col className={styles.item}>
                        <div>
                            <div>Following</div>
                            <div className={styles.itemAmount}>{followingCount === -1 ? "" : followingCount}</div>
                        </div>
                    </Col>
                    <Col className={styles.item}>
                        <div>
                            <div>Followers</div>
                            <div className={styles.itemAmount}>{followerCount === -1 ? "" : followerCount}</div>
                        </div>
                    </Col>
                </Row>
            </div>
            {/** Users feed */}
            <div id={styles.feed}>
                {authorId && <PostStream type={PostStreamTy.Author} authorID={authorId} postID={null} />}
            </div>
        </div>
    </Page>;
};

export default ProfilePage;
