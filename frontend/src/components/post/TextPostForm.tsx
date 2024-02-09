import { useState } from 'react';
import { Alert, Button, Form, ToggleButton, ToggleButtonGroup } from 'react-bootstrap';
import styles from './TextPostForm.module.css';
import { baseURL } from '../../constants';
import { useNavigate } from 'react-router-dom';

const TextPostForm: React.FC = () => {
    const [title, setTitle] = useState<string>('');
    const [description, setDescription] = useState<string>('');
    const [content, setContent] = useState<string>('');
    const [contentType, setContentType] = useState<string>('text/plain');
    const [visibility, setVisibility] = useState<string>('PUBLIC');
    const [formErrors, setFormErrors] = useState<{ [key: string]: string }>({});
    const [responseMessage, setResponseMessage] = useState<string>('');
    const navigate = useNavigate();

    /** function for handling form submission */
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (validateForm()) {
            const formData = new URLSearchParams({
                title: title,
                description: description,
                content: content,
                contentType: contentType,
                visibility: visibility
            }).toString();

            const response = await fetch(`${baseURL}/api/authors/<int:author_id>/posts`, {
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
    }

    /** function for validating form elements */
    const validateForm = () => {
        let isValid = true;
        const newFormErrors: { [key: string]: string } = {};

        if (!title) {
            isValid = false;
            newFormErrors.title = 'A title is required';
        }
        if (!description) {
            isValid = false;
            newFormErrors.description = 'A description is required';
        }
        if (!content) {
            isValid = false;
            newFormErrors.content = 'Post content is required';
        }

        setFormErrors(newFormErrors);
        return isValid;
    };
    
    return (
        <>
            {/** Alert for Request Errors */}
            {!!responseMessage ? (
                <Alert variant='danger' dismissible>
                    <Alert.Heading>An Error Occured When Sending Your Request To The Server</Alert.Heading>
                    <p>{responseMessage}</p>
                </Alert>
            ) : null}
            {/** Form */}
            <Form onSubmit={handleSubmit}>
                <div className={`${styles.selectToolbar} ${styles.formGroup}`}>
                    {/** Visibility Select */}
                    <ToggleButtonGroup
                        type='radio'
                        name='visibility-options'
                        defaultValue='PUBLIC'
                    >
                        <ToggleButton
                            id='visibility-radio-1'
                            value='PUBLIC'
                            onChange={(e) => setVisibility('PUBLIC')}
                            variant='secondary'
                            className={styles.radioSelectOption}
                        >
                            Public
                        </ToggleButton>
                        <ToggleButton
                            id='visibility-radio-2'
                            value='FRIENDS'
                            onChange={(e) => setVisibility('FRIENDS')}
                            variant='secondary'
                            className={styles.radioSelectOption}
                        >
                            Friends
                        </ToggleButton>
                        <ToggleButton
                            id='visibility-radio-3'
                            value='UNLISTED'
                            onChange={(e) => setVisibility('UNLISTED')}
                            variant='secondary'
                            className={styles.radioSelectOption}
                        >
                            Unlisted
                        </ToggleButton>
                    </ToggleButtonGroup>
                    {/** Content Type Select */}
                    <ToggleButtonGroup
                        type='radio'
                        name='ctype-options'
                        defaultValue='text/plain'
                    >
                        <ToggleButton
                            id='ctype-radio-1'
                            value='text/plain'
                            onChange={(e) => setContentType('text/plain')}
                            variant='secondary'
                            className={styles.radioSelectOption}
                        >
                            Plain
                        </ToggleButton>
                        <ToggleButton
                            id='ctype-radio-2'
                            value='text/markdown'
                            onChange={(e) => setContentType('text/markdown')}
                            variant='secondary'
                            className={styles.radioSelectOption}
                        >
                            Markdown
                        </ToggleButton>
                    </ToggleButtonGroup>
                </div>
                {/** Title Field */}
                <Form.Group className={styles.formGroup}>
                    <Form.Label className={styles.formLabel}>
                        Title
                    </Form.Label>
                    <Form.Control
                        type='text'
                        placeholder='Enter a Title for Your Post'
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        isInvalid={!!formErrors.title}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type='invalid'>
                        {formErrors.title}
                    </Form.Control.Feedback>
                </Form.Group>
                {/** Description Field */}
                <Form.Group className={styles.formGroup}>
                    <Form.Label className={styles.formLabel}>
                        Description
                    </Form.Label>
                    <Form.Control
                        type='text'
                        placeholder='Enter a Description for Your Post'
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        isInvalid={!!formErrors.description}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type='invalid'>
                        {formErrors.description}
                    </Form.Control.Feedback>
                </Form.Group>
                {/** Content Field */}
                <Form.Group className={styles.formGroup}>
                    <Form.Label className={styles.formLabel}>
                        Content
                    </Form.Label>
                    <Form.Control
                        as='textarea'
                        placeholder='Enter Your Post Here'
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        isInvalid={!!formErrors.content}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type='invalid'>
                        {formErrors.content}
                    </Form.Control.Feedback>
                </Form.Group>
                {/** Post Button */}
                <Button type='submit' className={styles.submitButton}>
                    Submit
                </Button>
            </Form>
        </>
    );
}

export default TextPostForm;