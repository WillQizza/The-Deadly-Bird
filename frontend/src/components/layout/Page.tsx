import React from "react";

import styles from "./Page.module.css";
import Footer from "./Footer";

const Page = ({ children } : { children: React.ReactNode }) => {
    return (
        <div id={styles.root}>
            <div id={styles.contentRoot}>
                <div id={styles.navigation}>
                    
                </div>
                <div id={styles.content}>
                    {children}
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default Page;