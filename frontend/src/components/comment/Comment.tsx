import { useState } from "react";
import styles from "./Comment.module.css";
import Markdown from "react-markdown";
import { ReactComponent as Heart } from 'bootstrap-icons/icons/heart.svg';
import { ReactComponent as HeartFilled } from 'bootstrap-icons/icons/heart-fill.svg';
import { Image } from "react-bootstrap";
import { apiCreateCommentLike } from "../../api/likes";

export interface CommentProps {
    id: string,
    postId: string,
    postAuthorId: string,
    authorId: string,
    authorName: string,
    profileImg: string,
    comment: string,
    contentType: string,
    date: string,
    likes: number,
    liked: boolean
}

const Comment: React.FC<CommentProps> = (props: CommentProps) => {
    const {
        id,
        postId,
        postAuthorId,
        authorId,
        authorName,
        profileImg,
        comment,
        contentType,
        date,
        likes,
        liked
    } = props;

    const [likeCount, setLikeCount] = useState(likes);
    const [isLiked, setIsLiked] = useState(liked);
    
    /** Function handling comment like */
    const handleLike = async () => {
        setIsLiked(true);
        setLikeCount(likeCount + 1);
        apiCreateCommentLike(postAuthorId, postId, id);
    }
    
    /** Comment */
    return (
        <div className={styles.commentContainer}>
            {/** Profile image of comment author */}
            <div className={styles.commentImageContainer}>
                <Image src={profileImg} roundedCircle width={50} height={50} />
            </div>
            {/** Comment info of comment  */}
            <div className={styles.commentInfoContainer}>
                <a href={`/profile/${authorId}`} className={styles.author}>@{authorName}</a>
                <p className={date}>{date}</p>
                {contentType == "text/markdown"? (
                    <Markdown className={styles.comment}>{comment}</Markdown>
                ) : (
                    <p className={styles.comment}>{comment}</p>
                )}
            </div>
            {/** Like for comment */}
            {/* TODO: part 3 */}
            {/* <div className={styles.likeContainer}>
                {isLiked
                    ? <HeartFilled className={`${styles.liked}`} />
                    : <Heart className={`${styles.like}`} onClick={handleLike}/>}
                <span>{likeCount}</span>
            </div> */}
        </div>
    );
}

export default Comment;