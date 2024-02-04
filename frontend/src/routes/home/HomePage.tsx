import React, { Fragment } from 'react';
import LoginForm from '../../components/login/LoginForm';

import styles from "./HomePage.module.css";
import Footer from '../../components/layout/Footer';

const HomePage: React.FC = () => {
    
    return ( 
        <Fragment>
            <div className={styles.HomePageContainer}>
                <div className={styles.imageColumn}>
                </div>
                <div className={styles.imageColorColumn}/>
                <div className={styles.loginColumn}>
                    <div className={styles.loginTitle}>
                        The Deadly Bird
                    </div>
                    <LoginForm />
                </div>
            </div>
            <Footer />
        </Fragment>
    );
};

export default HomePage;