import React from 'react';

import Page from '../../components/layout/Page';

import styles from './ProfilePage.module.css';

const ProfilePage: React.FC = () => {
    // GET request on user to request actual API?...
    return <Page>
        <div id={styles.container}>
            <div id={styles.header}>
                <div id={styles.information}>
                    <div id={styles.avatarContainer}>
                        <img src="" />
                    </div>
                    <div>
                        <h1 id={styles.username}>Username</h1>
                    </div>
                </div>
                <div id={styles.stats}>

                </div>
            </div>
            <div>
                {/* TODO: Profile feed */}
            </div>
        </div>
    </Page>;
};

export default ProfilePage;