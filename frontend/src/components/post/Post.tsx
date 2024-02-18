import React from 'react';
import styles from './Post.module.css';
import { publicDir } from "../../constants";
import { ReactComponent as ArrowRepeat } from 'bootstrap-icons/icons/arrow-repeat.svg';
import { ReactComponent as Heart } from 'bootstrap-icons/icons/heart.svg';

const Post: React.FC = () => {
    return (
        <div className={styles.postContainer}>
            {/* Header */}
            <div className={styles.postHeader}>
                {/* Profile picture */}
                <img className={styles.postProfilePicture} src={`${publicDir}/static/small-logo.png`}></img>
                {/* Post info */}
                <div className={styles.postInfo}>
                    {/* Author */}
                    <div className={styles.postAuthor}>@TheDeadlyBird</div>
                    {/* Sub info */}
                    <div className={styles.postSubInfo}>
                        {/* Date */}
                        <div className={styles.postSubInfoItem}>February 17th 2024, 11:25pm</div>
                        {/* Origin */}
                        <div className={styles.postSubInfoItem}>#deadlybird.xyz</div>
                    </div>
                </div>
            </div>
            {/* Body */}
            <div className={styles.postBody}>
                {/* Content */}
                <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</div>
                {/* Buttons */}
                <div className={styles.postButtons}>
                    {/* Share */}
                    <ArrowRepeat className={`${styles.postButton} ${styles.postShare}`}/>
                    {/* Like */}
                    <Heart className={`${styles.postButton} ${styles.postLike}`}/>
                </div>
            </div>
        </div>
    );
}

export default Post;
