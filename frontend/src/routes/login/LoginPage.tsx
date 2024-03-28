import React, { Fragment, useState, useEffect } from 'react';

import LoginForm from '../../components/login/LoginForm';
import RegisterForm from '../../components/login/RegisterForm';

import styles from "./LoginPage.module.css";
import Footer from '../../components/layout/Footer';

import { publicDir } from '../../constants';

const LoginPage: React.FC = () => {
    
    const [showLogin, setShowLogin] = useState<boolean>(true);
    const [authMessage, setAuthMessage] = useState<string>("Sign Up");

    /** Sets the authorization message */
    useEffect(() => {
        if (showLogin) {
            setAuthMessage("Sign Up");
        } else {
            setAuthMessage("Log in");
        }
    }, [showLogin]);

    /** Login page */
    return (
        <Fragment>
            <div className={styles.loginPageContainer}>
                {/** Logo column */}
                <div className={styles.imageColumn}>
                    <img src={`${publicDir}/static/homepage-logo.png`} alt="Description" />
                </div>
                <div className={styles.imageColorColumn}/>
                {/** Login/registration form column */}
                <div className={styles.loginColumn}>
                    <div className={styles.loginTitle}>
                       The Deadly Bird
                    </div>
                    { showLogin 
                        ? <LoginForm/> 
                        : <RegisterForm showLogin={showLogin} setShowLogin={setShowLogin}/>
                    }
                    <div onClick={() => setShowLogin(!showLogin)} style={{cursor: "pointer"}}>
                        { authMessage }
                    </div> 
                </div>
            </div>
            <Footer />
        </Fragment>
    );
};

export default LoginPage;