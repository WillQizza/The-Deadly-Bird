import React from 'react';

import styles from "./HomePage.module.css";
import Page from '../../components/layout/Page';
import Post from '../../components/post/Post'
import { useParams } from 'react-router-dom';
import { getUserId } from '../../utils/auth';

const HomePage: React.FC = () => {
    
    return ( 
        <Page>
            <div className="TEST_DIV"
            style={{color:'white', fontSize:'40px', margin:'auto'}} 
            >
                User: {getUserId()} Logged In!
            </div>

            <Post/>
        </Page>
    );
};

export default HomePage;
