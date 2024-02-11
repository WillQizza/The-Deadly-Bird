import React, { useState, useEffect } from 'react';

import { baseURL, publicDir } from "../../constants";

import Page from '../../components/layout/Page';

import styles from './ProfilePage.module.css';
import { apiRequest } from '../../utils/request';
import { useParams } from 'react-router-dom';

const ProfilePage: React.FC = () => {
    // GET request on user to request actual API?...
    const [avatarURL, setAvatarURL] = useState(`${publicDir}/static/default-avatar.png`);
    const [githubUsername, setGithubUsername] = useState("");
    const [username, setUsername] = useState("");
    const [bio, setBio] = useState("I don't really know what I'm doing...");     // TODO: Do we want a bio?
    const [postCount, setPostCount] = useState(-1);
    const [followingCount, setFollowingCount] = useState(-1);
    const [followerCount, setFollowerCount] = useState(-1);

    const params = useParams();

    useEffect(() => {
        const userId = params["id"];
        apiRequest(`${baseURL}/api/authors/${userId}/`)
            .then(async r => {
                if (r.status !== 200) {
                    console.error(`Failed to load user profile: ${userId} (status: ${r.status})`);
                    return;
                }

                const data = await r.json();
                setUsername(data["displayName"]);
                setGithubUsername(data["github"]);
                setPostCount(data["posts"]);
                setFollowerCount(data["followers"]);
                setFollowingCount(data["following"]);

                if (data["profileImage"] !== null) {
                    setAvatarURL(data["profileImage"]);
                }
            });
    }, [params]);

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
                        <div id={styles.followButton}>
                            Follow
                        </div>
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