import React from 'react';

import { publicDir } from "../../constants";

import Page from '../../components/layout/Page';

import styles from './ProfilePage.module.css';

const ProfilePage: React.FC = () => {
    // GET request on user to request actual API?...
    return <Page>
        <div id={styles.container}>
            <div id={styles.header} style={{ position: "relative" }}>
                <div id={styles.avatarContainer}>
                    <img alt="Profile Avatar" src="https://avatars.githubusercontent.com/u/46386037?s=48&v=4" />
                </div>
                <div id={styles.identityContainer}>
                    <h1 id={styles.username}>Username</h1>
                    <h5 id={styles.bio}>I don't really know what I'm doing...</h5>
                </div>
                <div id={styles.statsAndFollow}>
                    <div className={styles.item}>
                        <div id={styles.followButton}>
                            Follow
                        </div>
                    </div>
                    <div className={styles.item}>
                        <div>
                            <span>Posts</span> <span className={styles.itemAmount}>75</span>
                        </div>
                    </div>
                    <div className={styles.item}>
                        <div>
                            <span>Following</span> <span className={styles.itemAmount}>23</span>
                        </div>
                    </div>
                    <div className={styles.item}>
                        <div>
                            <span>Followers</span> <span className={styles.itemAmount}>73</span>
                        </div>
                    </div>
                </div>
                <div id={styles.githubContainer}>
                    <img alt="Github Account" style={{ height: "100%", width: "100%" }} src={`${publicDir}/static/github.png`} />
                </div>
            </div>
            <div id={styles.feed}>
                {/* TODO: Profile feed */}
            </div>
        </div>
    </Page>;
};

export default ProfilePage;