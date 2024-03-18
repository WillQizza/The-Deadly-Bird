import { useEffect, useRef, useState } from "react";
import { ListGroup, Image, Col, Row, Alert } from "react-bootstrap";
import { ReactComponent as Heart } from 'bootstrap-icons/icons/heart.svg';
import { ReactComponent as HeartFilled } from 'bootstrap-icons/icons/heart-fill.svg';
import Markdown from 'react-markdown';
import styles from "./CommentSection.module.css";
import { baseURL } from "../../constants";
import { apiRequest } from "../../utils/request";

interface CommentSectionProps {
    postId: string,
    authorId: string,
    updateCount: number  // indicates if the comment section needs to be updated
}

interface CommentProps {
    id: string,
    authorUrl: string,
    authorName: string,
    profileImg: string,
    comment: string,
    contentType: string,
    date: string,
    likes: number,
    isLiked: boolean
}

const CommentSection: React.FC<CommentSectionProps> = (props: CommentSectionProps) => {
    const { postId, authorId, updateCount } = props;
    const [comments, setComments] = useState<CommentProps[]>([]);
    const [responseMessage, setResponseMessage] = useState<string>("");
    const commentRef = useRef<HTMLAnchorElement>(null);
    const pageSize = 5;
    const currentPage = useRef(1);

    /** Function for fetching more comments */
    const fetchComments = async (reset?: boolean) => {
        // Request comments data
        const response = await apiRequest(
            `${baseURL}/api/authors/${authorId}/posts/${postId}/comments/?page=${currentPage.current}&size=${pageSize}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
            }
        );
        // Handle response
        const data = await response.json();
        if (response.ok) {
            let newComments: CommentProps[] = [];
            for (const commentData of data.comments) {
                newComments.push({
                    id: commentData.id,
                    authorUrl: commentData.author.url,
                    authorName: commentData.author.displayName,
                    profileImg: commentData.author.profileImage,
                    comment: commentData.comment,
                    contentType: commentData.contentType,
                    date: commentData.published,
                    likes: 0,
                    isLiked: false
                });
            }
            reset ? setComments(newComments) : setComments([...comments, ...newComments]);
        } else {
            setResponseMessage(data.message);
        }
    };

    /** Retrieves initial comments on mount */
    useEffect(() => {
        fetchComments();
    }, []);

    /** Retrieves comments while scrolling */
    useEffect(() => {
        // check if comments need generated
        if (Math.floor(comments.length / pageSize) < currentPage.current) {
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    currentPage.current++;
                    fetchComments();
                    observer.unobserve(entry.target);
                }
            });
        }, {
            root: null,
            threshold: 0,
        });

        // begin observe
        if (commentRef.current) {
            observer.observe(commentRef.current);
        }

        // cleanup function
        return () => {
            if (commentRef.current) {
                observer.unobserve(commentRef.current);
            }
        }
    }, [comments])

    /** Retrieves comments while scrolling */
    useEffect(() => {
        currentPage.current = 1;
        fetchComments(true);
    }, [updateCount])

    /** Comment section */
    return (
        <>
            {/** Alert for request errors */}
            {!!responseMessage ? (
                <Alert variant='danger' data-bs-theme='dark' dismissible>
                    <Alert.Heading>An Error Occured When Sending Your Request To The Server</Alert.Heading>
                    <hr />
                    <p>{responseMessage || 'An error occured'}</p>
                </Alert>
            ) : null}
            {/** Comments section */}
            <ListGroup>
                {comments.map((comment, index) => (
                    <ListGroup.Item key={comment.id} ref={index === comments.length - 1 ? commentRef : null}>
                        <div className={styles.commentContainer}>
                            <div className={styles.commentImageContainer}>
                                <Image src={comment.profileImg} roundedCircle width={50} height={50} />
                            </div>
                            <div className={styles.commentInfoContainer}>
                                <a href={comment.authorUrl} className={styles.author}>@{comment.authorName}</a>
                                <p className={styles.date}>{comment.date}</p>
                                {comment.contentType == "text/markdown"? (
                                    <Markdown className={styles.comment}>{comment.comment}</Markdown>
                                ) : (
                                    <p className={styles.comment}>{comment.comment}</p>
                                )}
                            </div>
                        </div>
                    </ListGroup.Item>
                ))}
            </ListGroup>

        </>
    );
}

export default CommentSection;