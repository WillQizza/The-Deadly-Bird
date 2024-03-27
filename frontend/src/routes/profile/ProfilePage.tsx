import React, { useState, useEffect } from 'react';
import { publicDir } from "../../constants";
import Page from '../../components/layout/Page';
import styles from './ProfilePage.module.css';
import { useParams } from 'react-router-dom';
import { apiGetAuthor } from '../../api/authors';
import { getUserId } from '../../utils/auth';
import { apiDeleteFollower, apiInboxFollowRequest, apiGetFollower, apiGetFollowRequest} from '../../api/following';
import PostStream, { PostStreamTy } from '../../components/post/PostStream';

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

    const loggedInAuthorId : string = getUserId()!; 
    const params = useParams();
    const userId = params["id"]!;

    /** Function to update the user's following */
    const updateFollowingState = async (userId: string) => {
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
    }

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

                if (author.github) {
                    setGithubUsername(author.github.substring("https://github.com/".length));
                }
                if (author.profileImage) {
                    setAvatarURL(author.profileImage);
                }
            });
        
        if (userId) { 
            updateFollowingState(userId);
        }
         
    }, [params]);

    /** Function to render the follow button based on following state */
    const renderButton = () => {
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
                        alert("Follow Request Already Pending!");
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
                            alert(`Failed to connect to remote host`);
                        } else { 
                            await updateFollowingState(authorId);
                            alert(`Follow Request Sent!`);
                        }
                    }}>
                        Follow
                    </button>
                );
        }
    };
    
    /** Profile page */
    return <Page selected="Profile">
        <div id={styles.container}>
            <div id={styles.header} style={{ position: "relative" }}>
                {/** Avatar */}
                <div id={styles.avatarContainer}>
                    <img alt="Profile Avatar" src={avatarURL} />
                </div>
                {/** About the user */}
                <div id={styles.identityContainer}>
                    <h1 id={styles.username}>{username}</h1>
                    <h5 id={styles.bio}>{bio}</h5>
                </div>
                {/** Following and post statistics */}
                <div id={styles.statsAndFollow}> 
                    <div className={styles.item}>
                        {renderButton()}
                    </div>
                    <div className={styles.item}>
                        <div>
                            <span>Posts</span> <span className={styles.itemAmount}>{postCount === -1 ? "" : postCount}</span>
                        </div>
                    </div>
                    <div className={styles.item}>
                        <div>
                            <span>Following</span> <span className={styles.itemAmount}>{followingCount === -1 ? "" : followingCount}</span>
                        </div>
                    </div>
                    <div className={styles.item}>
                        <div>
                            <span>Followers</span> <span className={styles.itemAmount}>{followerCount === -1 ? "" : followerCount}</span>
                        </div>
                    </div>
                </div>
                {/** Github section (if applicable) */}
                {githubUsername ? (
                    <a href={`https://github.com/${githubUsername}`} target="_blank" rel="noreferrer">
                        <div id={styles.githubContainer}>
                            <img alt="Github Account" style={{ height: "100%", width: "100%" }} src={`${publicDir}/static/github.png`} />
                        </div>
                    </a>
                ) : null}
            </div>
            {/** Users feed */}
            <div id={styles.feed}>
                {authorId && <PostStream type={PostStreamTy.Author} authorID={authorId} postID={null} />}
            </div>
        </div>
    </Page>;
};

export default ProfilePage;
