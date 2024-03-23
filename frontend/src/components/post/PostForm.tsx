import styles from './PostForm.module.css';
import { useEffect, useRef, useState } from 'react';
import { Alert, Button, Form, Modal } from 'react-bootstrap';
import { baseURL } from '../../constants';
import { useNavigate } from 'react-router-dom';
import { getUserId } from '../../utils/auth';
import { apiRequest } from '../../utils/request';
import FormTextbox from './FormTextbox';
import RadioButtonGroup from './RadioButtonGroup';
import ImageUpload from './ImageUpload';
import { apiDeletePosts } from '../../api/posts';
import DeleteDialog from './DeleteDialog';

interface PostFormProps {
    image?: boolean,
    postId?: string,
    edit?: boolean
}

const PostForm: React.FC<PostFormProps> = (props: PostFormProps) => {
    const { image = false, postId = '' } = props;
    const [isImage, setIsImage] = useState<boolean>(image);
    const [title, setTitle] = useState<string>('');
    const [description, setDescription] = useState<string>('');
    const [content, setContent] = useState<string>('');
    const [visibility, setVisibility] = useState<string>('PUBLIC');
    const [contentType, setContentType] = useState<string>('text/plain');
    const [formErrors, setFormErrors] = useState<{ [key: string]: string }>({});
    const [responseMessage, setResponseMessage] = useState<string>('');
    const [showConfirm, setShowConfirm] = useState(false);

    const navigate = useNavigate();

    /** Fills the post fields with existing values on mount if a post id is given  */
    useEffect(() => {
        /** Function for fetching the post's data */
        const fetchPostData = async () => {
            // Request post data
            const response = await apiRequest(
                `${baseURL}/api/authors/${getUserId()}/posts/${postId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                }
            );
            // Handle response
            const data = await response.json();
            if (response.ok) {
                setTitle(data.title);
                setDescription(data.description);
                setContent(data.content);
                setVisibility(data.visibility);
                setContentType(data.contentType);
                
                if (!data.contentType.startsWith('text')) {
                    setIsImage(true);
                }
            } else {
                setResponseMessage(data.message);
            }
        };

        // Fetch the post's data
        if (postId) {
            fetchPostData();
        }
    }, []);

    /** Function for handling form submission */
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (validateForm()) {
            // Send post update (if editing) or creation (if creating) request
            const formData = new URLSearchParams({
                title: title,
                description: description,
                content: content,
                contentType: contentType,
                visibility: visibility
            }).toString();

            const reqURL = postId ? `${baseURL}/api/authors/${getUserId()}/posts/${postId}` : `${baseURL}/api/authors/${getUserId()}/posts/`;
            const reqMethod = postId ? 'PUT' : 'POST';

            const response = await apiRequest(reqURL, {
                method: reqMethod,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });

            // Handle response
            if (response.ok) {
                navigate('/home');
            } else {
                const data = await response.json();
                setResponseMessage(data.message);
            }
        }
    };

    /** Function for validating form input */
    const validateForm = () => {
        let isValid = true;
        const newFormErrors: { [key: string]: string } = {};

        if (!title) {
            isValid = false;
            newFormErrors['title'] = 'A title is required';
        }
        if (title.length > 255) {
            isValid = false;
            newFormErrors['title'] = 'Title is too long (255 characters maximum)';
        }
        if (!description) {
            isValid = false;
            newFormErrors['description'] = 'A description is required';
        }
        if (description.length > 255) {
            isValid = false;
            newFormErrors['description'] = 'Description is too long (255 characters maximum)'
        }
        if (!content) {
            isValid = false;
            newFormErrors['content'] = 'Post content is required';
        }

        setFormErrors(newFormErrors);
        return isValid;
    };

    /** Function handling the delete button being clicked */
    const handleDeleteClick = () => {
        setShowConfirm(true);
    };

    /** Post form */
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
            <Form onSubmit={handleSubmit} data-bs-theme='dark'>
                <div className={`${styles.selectToolbar} ${styles.formGroup}`}>
                    {/** Visibility select */}
                    <RadioButtonGroup
                        name={`visibility-select/image=${isImage}`}
                        options={[
                            { value: 'PUBLIC', label: 'Public'},
                            { value: 'FRIENDS', label: 'Friends' },
                            { value: 'UNLISTED', label: 'Unlisted' }
                        ]}
                        value={visibility}
                        setValue={setVisibility}
                    />
                    {/** Content type select (only for text posts) */}
                    {isImage ? null : (
                        <RadioButtonGroup
                            name='ctype-select'
                            options={[
                                { value: 'text/plain', label: 'Plain' },
                                { value: 'text/markdown', label: 'Markdown' }
                            ]}
                            value={contentType}
                            setValue={setContentType}
                        />
                    )}
                </div>
                {/** Title field */}
                <FormTextbox
                    label='Title'
                    placeholder='Enter a Title for Your Post'
                    formErrors={formErrors}
                    formErrorKey={'title'}
                    value={title}
                    setValue={setTitle}
                />
                {/** Description field */}
                <FormTextbox
                    label='Description'
                    placeholder='Enter a Description for Your Post'
                    formErrors={formErrors}
                    formErrorKey={'description'}
                    value={description}
                    setValue={setDescription}
                />
                {/** Content field */}
                {isImage ? (
                    <ImageUpload
                        formErrors={formErrors}
                        setFormErrors={setFormErrors}
                        formErrorKey={'content'}
                        value={postId ? (`${baseURL}/api/authors/${getUserId()}/posts/${postId}/image`) : (content)}
                        setValue={setContent}
                        setType={setContentType}
                    />
                ) : (
                    <FormTextbox
                        label='Content'
                        placeholder='Enter Your Post Here'
                        formErrors={formErrors}
                        formErrorKey={'content'}
                        value={content}
                        setValue={setContent}
                        textarea={true}
                    />
                )}
                <div className={styles.submitToolbar}>
                    {/** Submit button */}
                    <Button type='submit' className={styles.submitButton}>
                        Submit
                    </Button>
                    {/** Delete button */}
                    { props.edit ?
                        <> 
                            <Button
                                variant={"danger"}
                                className={styles.deleteButton}
                                onClick={handleDeleteClick}
                            >
                                Delete
                            </Button>
                            <DeleteDialog
                                show={showConfirm}
                                setShow={setShowConfirm}
                                postId={postId}
                            />
                        </> 
                        : null
                    }
                </div>
            </Form>
        </>
    );
}

export default PostForm;