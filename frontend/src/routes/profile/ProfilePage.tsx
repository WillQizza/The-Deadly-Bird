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
                <div style={{ flexGrow: 1, display: "flex", justifyContent: "flex-end", gap: 10, marginRight: 10, marginBottom: 10 }}>
                    <div style={{ display: "flex", justifyContent: "flex-end", flexDirection: "column" }}>
                        <div style={{ border: "1px solid black", paddingTop: 2.5, paddingBottom: 2.5, paddingLeft: 30, paddingRight: 30 }}>
                            Follow
                        </div>
                    </div>
                    <div style={{ display: "flex", justifyContent: "flex-end", flexDirection: "column" }}>
                        <div>
                            <span style={{ fontSize: "1em" }}>Posts</span> <span style={{ fontSize: "1.5em" }}>75</span>
                        </div>
                    </div>
                    <div style={{ display: "flex", justifyContent: "flex-end", flexDirection: "column" }}>
                        <div>
                            <span style={{ fontSize: "1em" }}>Following</span> <span style={{ fontSize: "1.5em" }}>75</span>
                        </div>
                    </div>
                    <div style={{ display: "flex", justifyContent: "flex-end", flexDirection: "column" }}>
                        <div>
                            <span style={{ fontSize: "1em" }}>Followers</span> <span style={{ fontSize: "1.5em" }}>75</span>
                        </div>
                    </div>
                </div>
                <div style={{ position: "absolute", right: 0, top: 0, width: 48, height: 48, margin: 10 }}>
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