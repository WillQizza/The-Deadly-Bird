import React from "react";

import styles from "./Page.module.css";
import Footer from "./Footer";

import Navigation from "./Navigation";

const Page = ({ children } : { children: React.ReactNode }) => {
    return (
        <div id={styles.root}>
            <div id={styles.contentRoot}>
                <div id={styles.navigation}>
                    <Navigation items={[
                        { name: "Home", icon: "home", path: "/home" },
                        { name: "Profile", icon: "profile", path: "/profile" },
                        { name: "Network", icon: "network", path: "/network" },
                        { name: "Settings", icon: "settings", path: "/settings" }
                    ]} />
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