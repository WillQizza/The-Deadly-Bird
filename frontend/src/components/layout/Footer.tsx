import React from 'react';

import styles from "./Footer.module.css";

const Footer: React.FC = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.footerContainer}>
                <span>&copy; {new Date().getFullYear()} The Deadly Bird</span>
            </div>
        </footer>
    );
};

export default Footer;
