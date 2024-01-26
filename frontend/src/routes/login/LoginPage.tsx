import React, { Fragment } from 'react';
import LoginForm from '../../components/login/LoginForm';

import styles from "./LoginPage.module.css";
import Footer from '../../components/layout/Footer';

const LoginPage: React.FC = () => {
    
    const publicDir = process.env.PUBLIC_URL;

    return ( 
        <Fragment>
            <div className={styles.loginPageContainer}>
                <div className={styles.imageColumn}>
                    <img src={`${publicDir}/static/homepage-logo.png`} alt="Description" />
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

export default LoginPage;