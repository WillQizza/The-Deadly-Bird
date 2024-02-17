import styles from './PostForm.module.css';
import { useRef, useState } from 'react';
import { Alert, Button, Form } from 'react-bootstrap';
import { baseURL } from '../../constants';
import { useNavigate } from 'react-router-dom';
import { getUserId } from '../../utils/auth';
import { apiRequest } from '../../utils/request';
import FormTextbox from './FormTextbox';
import RadioButtonGroup from './RadioButtonGroup';
import ImageUpload from './ImageUpload';

interface PostFormProps {
    image?: boolean
}

const PostForm: React.FC<PostFormProps> = (props: PostFormProps) => {
    const { image = false } = props;
    const titleRef = useRef<string>('');
    const descriptionRef = useRef<string>('');
    const contentRef = useRef<string>('');
    const visibilityRef = useRef<string>('PUBLIC');
    const contentTypeRef = useRef<string>('text/plain');
    const [formErrors, setFormErrors] = useState<{ [key: string]: string }>({});
    const [responseMessage, setResponseMessage] = useState<string>('');
    const navigate = useNavigate();

    /** function for handling form submission */
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (validateForm()) {
            const formData = new URLSearchParams({
                title: titleRef.current,
                description: descriptionRef.current,
                content: contentRef.current,
                contentType: contentTypeRef.current,
                visibility: visibilityRef.current
            }).toString();

            const response = await apiRequest(`${baseURL}/api/authors/${getUserId()}/posts/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });

            if (response.ok) {
                navigate('/home');
            } else {
                const data = await response.json();
                setResponseMessage(data.message);
            }
        }
    };

    /** function for validating form elements */
    const validateForm = () => {
        let isValid = true;
        const newFormErrors: { [key: string]: string } = {};

        if (!titleRef.current) {
            isValid = false;
            newFormErrors['title'] = 'A title is required';
        }
        if (!descriptionRef.current) {
            isValid = false;
            newFormErrors['description'] = 'A description is required';
        }
        if (!contentRef.current) {
            isValid = false;
            newFormErrors['content'] = 'Post content is required';
        }

        setFormErrors(newFormErrors);
        return isValid;
    };
    
    return (
        <>
            {/** Alert for Request Errors */}
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
                    {/** Visibility Select */}
                    <RadioButtonGroup
                        name='visibility-select'
                        defaultValue='PUBLIC'
                        options={[
                            { value: 'PUBLIC', label: 'Public'},
                            { value: 'FRIENDS', label: 'Friends' },
                            { value: 'UNLISTED', label: 'Unlisted' }
                        ]}
                        valueRef={visibilityRef}
                    />
                    {/** Content Type Select (only for text posts) */}
                    {image ? null : (
                        <RadioButtonGroup
                            name='ctype-select'
                            defaultValue='text/plain'
                            options={[
                                { value: 'text/plain', label: 'Plain' },
                                { value: 'text/markdown', label: 'Markdown' }
                            ]}
                            valueRef={contentTypeRef}
                        />
                    )}
                </div>
                {/** Title Field */}
                <FormTextbox
                    label='Title'
                    placeholder='Enter a Title for Your Post'
                    formErrors={formErrors}
                    formErrorKey={'title'}
                    valueRef={titleRef}
                />
                {/** Description Field */}
                <FormTextbox
                    label='Description'
                    placeholder='Enter a Description for Your Post'
                    formErrors={formErrors}
                    formErrorKey={'description'}
                    valueRef={descriptionRef}
                />
                {/** Content Field */}
                {image ? (
                    <ImageUpload
                        formErrors={formErrors}
                        formErrorKey={'content'}
                        valueRef={contentRef}
                        typeRef={contentTypeRef}
                    />
                ) : (
                    <FormTextbox
                        label='Content'
                        placeholder='Enter Your Post Here'
                        formErrors={formErrors}
                        formErrorKey={'content'}
                        valueRef={contentRef}
                        textarea={true}
                    />
                )}
                {/** Post Button */}
                <Button type='submit' className={styles.submitButton}>
                    Submit
                </Button>
            </Form>
        </>
    );
}

export default PostForm;