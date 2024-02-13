import React from 'react';

import styles from "./NetworkPage.module.css";
import Page from '../../components/layout/Page';
import ExploreView from './ExploreView';

const NetworkPage: React.FC = () => {
    return (
        <Page>
            <div className={styles.mainHeader}>Network</div>
            <div className={styles.subHeader}>Explore the Deadly Bird Network</div>

            <div id={styles.NetworkExploreHeader}>
                Explore Local Authors
            </div>
            <ExploreView />

            <div id={styles.NetworkExploreHeader}>
                Explore Remote Authors
            </div>
            <ExploreView />
        </Page>
    );
};

export default NetworkPage;