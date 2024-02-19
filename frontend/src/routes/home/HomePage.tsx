import React from 'react';

import styles from "./HomePage.module.css";
import Page from '../../components/layout/Page';
import Post from '../../components/post/Post'

const HomePage: React.FC = () => {
    
    return ( 
        <Page>
            <Post/>
        </Page>
    );
};

export default HomePage;
