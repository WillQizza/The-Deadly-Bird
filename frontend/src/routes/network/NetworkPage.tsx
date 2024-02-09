import React from 'react';

import styles from "./NetworkPage.module.css";
import Page from '../../components/layout/Page';
import NetworkExploreView from '../../components/layout/NetworkExploreView';

const NetworkPage: React.FC = () => {
    
    return ( 
        <Page>
            <NetworkExploreView />
        </Page>
    );
};

export default NetworkPage;