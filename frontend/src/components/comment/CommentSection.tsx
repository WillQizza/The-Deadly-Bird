import { useEffect, useRef, useState } from "react";
import { ListGroup, Alert } from "react-bootstrap";
import Comment from "./Comment";
import { CommentProps } from "./Comment";
import { getUserId } from "../../utils/auth";
import { apiGetCommentLikes } from "../../api/likes";
import { apiGetComments } from "../../api/comments";
import { extractAuthorIdFromApi } from "../../api/utils";

interface CommentSectionProps {
    postId: string,
    authorId: string,
    refresh: boolean  // indicates if the comment section needs to be refreshed
    setRefresh: React.Dispatch<React.SetStateAction<boolean>>
}

const CommentSection: React.FC<CommentSectionProps> = (props: CommentSectionProps) => {
    const { postId, authorId, refresh, setRefresh } = props;
    const [comments, setComments] = useState<CommentProps[]>([]);
    const commentRef = useRef<HTMLAnchorElement>(null);
    const pageSize = 5;
    const currentPage = useRef(1);
    const [responseMessage, setResponseMessage] = useState<string>("");

    /** Function for fetching more comments */
    const fetchComments = async (reset?: boolean) => {
        // Handle response
        const data = await apiGetComments(authorId, postId, currentPage.current, pageSize);
        if (data["error"]) {
            setResponseMessage(data.message);
            return;
        }

        console.log("FETHCED COMMENTS", data);

        let newComments: CommentProps[] = [];
        for (const commentData of (data.comments || data.items)) {
            // const likeData = await apiGetCommentLikes(authorId, postId, commentData.id);
            newComments.push({
                id: commentData.id,
                postAuthorId: authorId,
                postId: postId,
                authorId: commentData.author.id,
                authorName: commentData.author.displayName,
                profileImg: commentData.author.profileImage,
                comment: commentData.comment,
                contentType: commentData.contentType,
                date: commentData.published,
                likes: 0, // likeData.length,
                liked: false, // !!likeData.find(like => extractAuthorIdFromApi(like.author.id) === getUserId())
            });
        }
        reset ? setComments(newComments) : setComments([...comments, ...newComments]);
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

    /** Re-retrieves comments after a comment has been made */
    useEffect(() => {
        if (refresh) {
            currentPage.current = 1;
            fetchComments(true);
            setRefresh(false);
        }
    }, [refresh])

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
                        <Comment {...comment} />
                    </ListGroup.Item>
                ))}
            </ListGroup>

        </>
    );
}

export default CommentSection;