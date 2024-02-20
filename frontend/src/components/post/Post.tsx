import React from 'react';
import styles from './Post.module.css';
import { Post as PostTy } from '../../api/types'
import { publicDir } from "../../constants";
import { ReactComponent as ArrowRepeat } from 'bootstrap-icons/icons/arrow-repeat.svg';
import { ReactComponent as Heart } from 'bootstrap-icons/icons/heart.svg';

const Post: React.FC<PostTy> = (props: PostTy) => {
    // Set profile picture src
    let profileImgSrc: string = '';
    // Make sure profile image field exists and is not null or empty
    if ('profileImage' in props.author && props.author.profileImage && props.author.profileImage.trim() !== '') {
        profileImgSrc = props.author.profileImage;
    }
    return (
        <div className={styles.postContainer}>
            {/* Header */}
            <div className={styles.postHeader}>
                {/* Profile picture */}
                <img className={styles.postProfilePicture} src={profileImgSrc}></img>
                {/* Post info */}
                <div className={styles.postInfo}>
                    {/* Author */}
                    <div className={styles.postAuthor}>{props.author.displayName}</div>
                    {/* Sub info */}
                    <div className={styles.postSubInfo}>
                        {/* Date */}
                        <div className={styles.postSubInfoItem}>{props.published_date}</div>
                        {/* Origin */}
                        <div className={styles.postSubInfoItem}>{props.origin}</div>
                    </div>
                </div>
            </div>
            {/* Body */}
            <div className={styles.postBody}>
                {/* Content */}
                <div>{props.content}</div>
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
