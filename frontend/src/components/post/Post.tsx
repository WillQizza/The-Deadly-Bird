import React from 'react';
import Markdown from 'react-markdown';
import styles from './Post.module.css';
import { ContentType, PostResponse } from '../../api/types'
import { baseURL, publicDir } from "../../constants";
import { ReactComponent as ArrowRepeat } from 'bootstrap-icons/icons/arrow-repeat.svg';
import { ReactComponent as Heart } from 'bootstrap-icons/icons/heart.svg';
import { ReactComponent as PencilSquare} from 'bootstrap-icons/icons/pencil-square.svg';
import { getUserId } from '../../utils/auth';

const Post: React.FC<PostResponse> = (props: PostResponse) => {
    // Set profile picture src
    let profileImgSrc: string = '';
    // Make sure profile image field exists and is not null or empty
    if ('profileImage' in props.author && props.author.profileImage && props.author.profileImage.trim() !== '') {
        profileImgSrc = props.author.profileImage;
    } else {
        profileImgSrc = `${publicDir}/static/default-avatar.png`;
    }

    // Format post date
    let postDate = new Date(props.published).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
    });

    // Determine post content format
    let content;
    switch (props.contentType) {
        case ContentType.MARKDOWN:
            content = <Markdown>{props.content}</Markdown>;
            break;
        case ContentType.PLAIN:
            content = <span>{props.content}</span>;
            break;
        case ContentType.APPLICATION_BASE64:
        case ContentType.PNG_BASE64:
        case ContentType.JPEG_BASE64:
            content = <img style={{ maxWidth: "100%" }} src={`${baseURL}/api/authors/${props.author.id}/posts/${props.id}/image`} alt="Image Post" />;
            break;
        default:
            content = <span>{props.content}</span>;
            break;
    }

    const handleLike = async () => {
        console.log("Liked!");
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
                    <div className={styles.postAuthor}>@{props.author.displayName}</div>
                    {/* Sub info */}
                    <div className={styles.postSubInfo}>
                        {/* Date */}
                        <div className={styles.postSubInfoItem}>{postDate}</div>
                        {/* Origin */}
                        <div className={styles.postSubInfoItem}>{props.origin}</div>
                    </div>
                </div>
            </div>
            {/* Body */}
            <div className={styles.postBody}>
                {/* Title */}
                <div className={styles.postTitle}>{props.title}</div>
                <div className={styles.postDescr}>{props.description}</div>
                {/* Content */}
                <div className={styles.postContent}>{content}</div>
                {/* Buttons */}
                <div className={styles.postButtons}>
                    {/* Share */}
                    <ArrowRepeat className={`${styles.postButton} ${styles.postShare}`}/>
                    {/* Like */}
                    <Heart className={`${styles.postButton} ${styles.postLike}`} onClick={handleLike}/>
                    {/* Edit */}
                    {
                        (props.author.id == getUserId()) ? (
                            <PencilSquare
                                className={`${styles.postButton} ${styles.postEdit}`}
                                onClick={(e) => {
                                    document.location.href = `/post/${props.id}`;
                                }}
                            />
                        ) : null
                    }
                </div>
            </div>
        </div>
    );
}

export default Post;
