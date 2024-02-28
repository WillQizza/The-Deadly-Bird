import React from 'react';

import styles from "./NetworkPage.module.css";
import Page from '../../components/layout/Page';
import ExploreView from './ExploreView';

const NetworkPage: React.FC = () => {
    /** Network page */
    return (
        <Page selected="Network">
            <div className={styles.networkPageContainer}>
                {/** Headers */}
                <div className={styles.mainHeader}>Network</div>
                <div className={styles.subHeader}>Explore the Deadly Bird Network</div>

                {/** Local authors */}
                <div id={styles.NetworkExploreHeader}>
                    Explore Local Authors
                </div>
                <ExploreView viewType="local"/>
                {/** Remote authors */}
                <div id={styles.NetworkExploreHeader}>
                    Explore Remote Authors
                </div>
                <ExploreView viewType="remote"/>
            </div>
        </Page>
    );
};

export default NetworkPage;