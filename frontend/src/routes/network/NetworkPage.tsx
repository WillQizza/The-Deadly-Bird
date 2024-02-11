import React from 'react';

import styles from "./NetworkPage.module.css";
import Page from '../../components/layout/Page';
import ExploreView from './ExploreView';

const NetworkPage: React.FC = () => {
    
    return ( 
        <Page>
            <div id={styles.NetworkPageHeader}>
                Explore the Deadly Bird Network
            </div>
            <ExploreView/>
        </Page>
    );
};

export default NetworkPage;