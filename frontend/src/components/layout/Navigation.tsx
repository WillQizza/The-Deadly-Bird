import React, { Fragment } from 'react';
import { publicDir } from "../../constants";
import styles from "./Navigation.module.css";
import { ReactComponent as CreatePost } from 'bootstrap-icons/icons/plus-circle.svg';
import { useNavigate } from 'react-router-dom';

type NavItem = {
    name: string;
    path: string;
    icon: React.ElementType;
};

export type SelectedNavigation = "Home" | "Profile" | "Network" | "Settings";


const Navigation = ({ items, selected }: { items: NavItem[], selected?: SelectedNavigation }) => {
    // return <Fragment>
    const navigate = useNavigate();

    /** Navigation bar */
    return (
        <div id={styles.navigationContainer}>
            {/** Logo */}
            <div id={styles.logoContainer}>
                <img src={`${publicDir}/static/small-logo.png`} alt="Description" />
            </div>

            {/** Navigation buttons */}
            <div id={styles.buttons}>
                {items.map((item, index) => (
                    <a className={styles.buttonLink} href={item.path} key={index}>
                        <div className={`${styles.button} ${selected === item.name ? styles.selected : ''}`}>
                            <div className={styles.icon}>
                                <item.icon/>
                            </div>
                            <div className={styles.text}>
                                <div>{item.name}</div>
                            </div>
                        </div>
                    </a>
                ))}
            </div>
            
            {/** Create post button */}
            <div id={styles.createPost}
                onClick={() => {navigate("/post")}}>
                <div id={styles.createPostIcon}>
                    <CreatePost
                        className={`${styles.postButton} ${styles.postCreate}`} 
                    />
                </div>
                
                Post
            </div>
        </div>
    ); 
};

export default Navigation;
