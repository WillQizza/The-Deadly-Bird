import React, { useState, useRef } from 'react';
import Markdown from 'react-markdown';
import styles from './Post.module.css';
import { ContentType, Post as PostTy } from '../../api/types'
import { baseURL, publicDir } from "../../constants";
import { ReactComponent as ArrowRepeat } from 'bootstrap-icons/icons/arrow-repeat.svg';
import { ReactComponent as Heart } from 'bootstrap-icons/icons/heart.svg';
import { ReactComponent as HeartFilled } from 'bootstrap-icons/icons/heart-fill.svg';
import { ReactComponent as PencilSquare} from 'bootstrap-icons/icons/pencil-square.svg';
import { ReactComponent as LinkIcon} from 'bootstrap-icons/icons/link-45deg.svg';
import { ReactComponent as Chat } from 'bootstrap-icons/icons/chat.svg';
import { ReactComponent as Trash } from 'bootstrap-icons/icons/trash3.svg';
import { getUserId } from '../../utils/auth';
import { apiCreatePostLike } from '../../api/likes';
import { Row, Col, Offcanvas, Overlay, Tooltip } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { apiSharePost } from '../../api/posts';
import CommentForm from '../comment/CommentForm';
import CommentSection from '../comment/CommentSection';
import DeleteDialog from './DeleteDialog';
import { extractAuthorIdFromApi, extractPostIdFromApi } from '../../api/utils';

type PostOptions = PostTy & {
    likes: number;
    isLiked: boolean;
    refreshStream: () => void;
};

const Post: React.FC<PostOptions> = props => {
    // Handle link button tooltip popup
    const linkButton = useRef(null);
    const [linkTooltipShow, setLinkTooltipShow] = useState(false);

    const postAuthor = props.originAuthor || props.author;

    // Set profile picture src
    // Make sure profile image field exists and is not null or empty
    let profileImgSrc: string = `${publicDir}/static/default-avatar.png`;
    if ('profileImage' in postAuthor && postAuthor.profileImage && postAuthor.profileImage.trim() !== '') {
        profileImgSrc = postAuthor.profileImage;
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

    const [likeCount, setLikeCount] = useState(props.likes);
    const [isLiked, setIsLiked] = useState(props.isLiked);

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
            content = <img style={{ maxWidth: "100%" }} src={`${baseURL}/api/authors/${extractAuthorIdFromApi(postAuthor.id)}/posts/${props.id}/image`} alt="Image Post" />;
            break;
        default:
            content = <span>{props.content}</span>;
            break;
    }

    /** Function handling post like */
    const handleLike = async () => {
        setIsLiked(true);
        setLikeCount(likeCount + 1);
        await apiCreatePostLike(props.author.id, props.id);
    }

    const handleShare = async () => {
        await apiSharePost(props.author.id, props.id);
        props.refreshStream();
    };

    // Handle comment section and commenting
    const [showComments, setShowComments] = useState(false);
    const [refreshComments, setRefreshComments] = useState(false);

    // Handle edit
    const [showConfirm, setShowConfirm] = useState(false);

    /** Function rendering edit button (or lack thereof) depending on the user */
    const EditButton = () => {
        if (extractAuthorIdFromApi(postAuthor.id) === getUserId()) {
            // edit button if they are the author of the post
            return(
                <Col className={styles.postButtonContainer}>
                    <PencilSquare
                        className={`${styles.postButton} ${styles.postEdit}`}
                        onClick={(e) => {
                            document.location.href = `/post/${extractPostIdFromApi(extractPostIdFromApi(props.originId || props.id))}`;
                        }}
                    />
                </Col>
            );
        }
        else if (props.originAuthor && extractAuthorIdFromApi(props.author.id) === getUserId()) {
            // delete button if they shared the post
            return(
                <Col className={styles.postButtonContainer}>
                    <Trash 
                        className={`${styles.postButton} ${styles.postDelete}`}
                        onClick={() => setShowConfirm(true)}
                    />
                    <DeleteDialog
                        show={showConfirm}
                        setShow={setShowConfirm}
                        postId={props.id}
                        onDelete={props.refreshStream}
                    />
                </Col>
            );
        }
        else {
            return null;
        }
    }

    /** Post */
    return (
        <div className={styles.postContainer}>
            {/* Header */}
            <Row className={styles.postHeader}>
                {/* Profile picture */}
                <Col className={"flex-grow-0"}>
                    <Link to={`/profile/${extractAuthorIdFromApi(extractAuthorIdFromApi(postAuthor.id))}`}>
                        <img className={styles.postProfilePicture} src={profileImgSrc}/>
                    </Link>
                </Col>
                {/* Post info */}
                <Col className={"flex-grow-1"}>
                    <div className={styles.postInfo}>
                        {/* Author */}
                        <Link to={`/profile/${extractAuthorIdFromApi(extractAuthorIdFromApi(postAuthor.id))}`} className={styles.postAuthor}>@{postAuthor.displayName}</Link>
                        {/* Sub info */}
                        <div className={styles.postSubInfo}>
                            {/* Date */}
                            <div className={styles.postSubInfoItem}>{postDate}</div>
                        </div>
                    </div>
                </Col>
            </Row>
            {/* Body */}
            <div className={styles.postBody}>
                {/* Title */}
                <div className={styles.postTitle}>{props.title}</div>
                <div className={styles.postDescr}>{props.description}</div>
                {/* Content */}
                <div className={styles.postContent}>{content}</div>
                {/* Buttons */}
                <Row className={styles.postButtons}>
                    {/* Share */}
                    {props.visibility === "PUBLIC" && (
                        <Col className={styles.postButtonContainer}>
                            <ArrowRepeat
                                className={`${styles.postButton} ${styles.postShare}`}
                                onClick={handleShare}
                            />
                        </Col>
                    )}
                    {/* Copy Link */}
                    <Col className={styles.postButtonContainer}>
                        <LinkIcon
                            ref={linkButton}
                            className={`${styles.postButton} ${styles.postLink}`}
                            onClick={() => {
                                // Copy post link to user clipboard
                                if (navigator.clipboard) {
                                    navigator.clipboard.writeText(`${window.location.origin}/profile/${extractAuthorIdFromApi(extractAuthorIdFromApi(props.author.id))}/posts/${props.id}`);
                                    setLinkTooltipShow(true);
                                }
                            }}
                            onMouseLeave={() => setLinkTooltipShow(false)}
                        />
                        <Overlay target={linkButton.current} show={linkTooltipShow} placement="bottom">
                            <Tooltip id="link-tooltip">
                                Link copied!
                            </Tooltip>
                        </Overlay>
                    </Col>
                    {/* Like */}
                    <Col className={styles.postButtonContainer}>
                        {isLiked
                            ? <HeartFilled className={`${styles.postButton} ${styles.postLiked}`} />
                            : <Heart className={`${styles.postButton} ${styles.postLike}`} onClick={handleLike}/>}
                        <span className={styles.likeCount}>{likeCount}</span>
                    </Col>
                    {/** Comment */}
                    <Col className={styles.postButtonContainer}>
                        <Chat
                            className={`${styles.postButton} ${styles.postComment}`}
                            onClick={() => setShowComments(true) }
                        />
                        <Offcanvas show={showComments}
                            onHide={() => setShowComments(false)}
                            placement="bottom"
                            scroll={true}
                            backdrop={true}
                            className={"h-75"}
                            data-bs-theme={"dark"}
                        >
                            <Offcanvas.Header closeButton>
                            <Offcanvas.Title>Comment Section</Offcanvas.Title>
                            </Offcanvas.Header>
                            <Offcanvas.Body>
                                <CommentSection
                                    postId={props.id}
                                    authorId={props.author.id}
                                    refresh={refreshComments}
                                    setRefresh={setRefreshComments}
                                />
                            </Offcanvas.Body>
                            <CommentForm
                                postId={props.id}
                                authorId={props.author.id}
                                refreshCommentStream={() => setRefreshComments(true)}
                            />
                        </Offcanvas>
                    </Col>
                    {/* Edit */}
                    <EditButton />
                </Row>
            </div>
        </div>
    );
}

export default Post;
