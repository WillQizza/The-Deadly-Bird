import React from 'react';

import styles from "./NetworkPage.module.css";
import Page from '../../components/layout/Page';
import ExploreView from './ExploreView';

const NetworkPage: React.FC = () => {
    
    return ( 
        <Page>
            <ExploreView />
        </Page>
    );
};

export default NetworkPage;