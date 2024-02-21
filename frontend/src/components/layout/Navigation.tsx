import React, { Fragment } from 'react';

import { publicDir } from "../../constants";

import styles from "./Navigation.module.css";

type NavItem = {
    name: string;
    path: string;
    icon: string;
};

export type SelectedNavigation = "Home" | "Profile" | "Network" | "Settings";


const Navigation = ({ items, selected }: { items: NavItem[], selected?: SelectedNavigation }) => {
    return <Fragment>
        <div id={styles.logoContainer}>
            <img src={`${publicDir}/static/small-logo.png`} alt="Description" />
        </div>

        <div id={styles.buttons}>
            {items.map((item, index) => (
                <a className={styles.buttonLink} href={item.path} key={index}>
                    <div className={`${styles.button} ${selected === item.name ? styles.selected : ''}`}>
                        <div className={styles.icon}>
                            <img src={`${publicDir}/static/nav/${item.icon}.png`} alt="Icon" />
                        </div>
                        <div className={styles.text}>
                            <div>{item.name}</div>
                        </div>
                    </div>
                </a>
            ))}
        </div>
    </Fragment>;
};

export default Navigation;