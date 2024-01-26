import React, {useState} from 'react';
import LoginForm from './LoginForm';

const LoginPage: React.FC = () => {
    
    const publicDir = process.env.PUBLIC_URL;

    return ( 
        <div className="LoginPageContainer">
            <div className="imageColumn">
                <img src={`${publicDir}/static/homepage-logo.png`} alt="Description" />
            </div>
            <div className="imageColorColumn"/>
            <div className="loginColumn">
                <div className="loginTitle">
                    The Deadly Bird
                </div>
                <LoginForm/>
            </div>
        </div>
    );
};

export default LoginPage;