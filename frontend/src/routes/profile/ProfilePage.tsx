import React, { useState, useEffect, lazy } from 'react';
import { publicDir } from "../../constants";
import Page from '../../components/layout/Page';
import styles from './ProfilePage.module.css';
import { useParams } from 'react-router-dom';
import { getAuthor } from '../../api/authors';
import { getUserId } from '../../utils/auth';
import { apiDeleteFollower, apiFollowRequest, apiGetFollower} from '../../api/following';
import { Button } from 'react-bootstrap';

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
    const [bio, setBio] = useState("I don't really know what I'm doing...");     // TODO: Do we want a bio?
    const [postCount, setPostCount] = useState(-1);
    const [followingCount, setFollowingCount] = useState(-1);
    const [followerCount, setFollowerCount] = useState(-1);
    const [followState, setFollowState] = useState<FollowState>(FollowState.NOT_FOLLOWING)

    const curAuthorId : string = getUserId().toString(); 
    const params = useParams();

    useEffect(() => {
        const userId = params["id"];
        getAuthor(parseInt(userId as string))
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

                if (author.github) {
                    setGithubUsername(author.github);
                }
                if (author.profileImage) {
                    setAvatarURL(author.profileImage);
                }
            });
        
        if (userId) { 
            // If logged in user is following viewed profile, set followState accoordingly
            apiGetFollower(userId, curAuthorId)
            .then(async response => {
                if (response.status != 404) { 
                    setFollowState(FollowState.FOLLOWING);
                } else {
                    // TODO: check if follow request is pending
                }
            });
        }
         
    }, [params]);

    const renderButton = () => {
        switch (followState) {
            case FollowState.FOLLOWING:
                return (
                    <button className="btn btn-danger" onClick={async () => {
                        await apiDeleteFollower(authorId, curAuthorId)
                            .then(status => {
                                if (status && status === 204) {
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
            case FollowState.NOT_FOLLOWING:
                return (
                    <button className="btn btn-primary" onClick={async () => {
                        await apiFollowRequest(curAuthorId, authorId)
                            .then(res => {
                                if (res && !res["error"]) {
                                    setFollowState(FollowState.PENDING);
                                }
                            }); 
                    }}>
                        Follow
                    </button>
                );
        }
    };
    
    return <Page>
        <div id={styles.container}>
            <div id={styles.header} style={{ position: "relative" }}>
                <div id={styles.avatarContainer}>
                    <img alt="Profile Avatar" src={avatarURL} />
                </div>
                <div id={styles.identityContainer}>
                    <h1 id={styles.username}>{username}</h1>
                    <h5 id={styles.bio}>{bio}</h5>
                </div>
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
                {githubUsername ? (
                    <a href={`https://github.com/${githubUsername}`} target="_blank" rel="noreferrer">
                        <div id={styles.githubContainer}>
                            <img alt="Github Account" style={{ height: "100%", width: "100%" }} src={`${publicDir}/static/github.png`} />
                        </div>
                    </a>
                ) : null}
            </div>
            <div id={styles.feed}>
                {/* TODO: Profile feed */}
            </div>
        </div>
    </Page>;
};

export default ProfilePage;