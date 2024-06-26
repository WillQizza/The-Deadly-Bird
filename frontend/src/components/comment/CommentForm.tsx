import { Button, Form, FloatingLabel, Alert } from "react-bootstrap";
import styles from "./CommentForm.module.css"
import { useState } from "react";
import { ReactComponent as SendIcon} from 'bootstrap-icons/icons/send.svg';
import { apiPostComment } from "../../api/comments";

interface CommentFormProps {
    postId: string,
    authorId: string,
    refreshCommentStream: () => void;
}

const CommentForm: React.FC<CommentFormProps> = (props: CommentFormProps) => {
    const { postId, authorId, refreshCommentStream } = props;
    const [comment, setComment] = useState("");
    const [type, setType] = useState("text/plain");
    const [error, setError] = useState("");
    const [responseMessage, setResponseMessage] = useState("");

    /** Function for handling form submission */
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        // Handle comment input
        if (comment) {
            // Send request for commenting on post
            const data = await apiPostComment(authorId, postId, { comment, contentType: type });

            // Handle response
            if (!data["error"]) {
                setComment("");
                refreshCommentStream();
            } else {
                setResponseMessage(data.message);
            }
        } else {
            setError("A comment is required");
        }
    }

    /** Comment form */
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
            {/** Form */}
            <Form onSubmit={handleSubmit} className={styles.formContainer}>
                {/** Comment input */}
                <FloatingLabel label="Enter Your Comment" className={styles.commentInputContainer}>
                    {/** Input */}
                    <Form.Control
                        placeholder=""
                        as="textarea"
                        value={comment}
                        onChange={(e) => setComment(e.target.value)}
                        isInvalid={!!error}
                        className={styles.commentInput}
                    />
                    {/** Error message */}
                    <Form.Control.Feedback type="invalid">
                        {error}
                    </Form.Control.Feedback>
                </FloatingLabel>
                {/** Form toolbar */}
                <div className={styles.commentFormToolbar}>
                    {/** Type edit */}
                    <Form.Select
                        defaultValue="text-plain"
                        size="sm"
                        onChange={(e) => setType(e.target.value) }
                    >
                        <option value="text/plain">Plain</option>
                        <option value="text/markdown">Markdown</option>
                    </Form.Select>
                    {/** Comment button */}
                    <Button
                        type="submit"
                        variant="outline-secondary"
                    >
                        <SendIcon/>
                    </Button>
                </div>
            </Form>
        </>
    );
}

export default CommentForm;