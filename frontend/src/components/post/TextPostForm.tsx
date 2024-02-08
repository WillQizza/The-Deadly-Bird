import { useState } from 'react';
import { Button, Form, ToggleButton, ToggleButtonGroup } from 'react-bootstrap';
import styles from './TextPostForm.module.css';

const TextPostForm: React.FC = () => {
    const [title, setTitle] = useState<string>('');
    const [description, setDescription] = useState<string>('');
    const [content, setContent] = useState<string>('');
    const [contentType, setContentType] = useState<string>('text/plain');
    const [visibility, setVisibility] = useState<string>('public');
    const [errors, setErrors] = useState<{ [key: string]: string }>({});

    /** function for handling form submission */
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (validateForm()) {
            
        }
    }

    /** function for validating form elements */
    const validateForm = () => {
        let isValid = true;
        const newErrors: { [key: string]: string } = {};

        if (!title) {
            isValid = false;
            newErrors.title = 'A title is required';
        }
        if (!description) {
            isValid = false;
            newErrors.description = 'A description is required';
        }
        if (!content) {
            isValid = false;
            newErrors.content = 'Post content is required';
        }

        setErrors(newErrors);
        return isValid;
    };
    
    return (
        <Form onSubmit={handleSubmit}>
            <div className={`${styles.selectToolbar} ${styles.formGroup}`}>
                {/** Visibility Select */}
                <ToggleButtonGroup
                    type='radio'
                    name='visibility-options'
                    defaultValue='public'
                >
                    <ToggleButton
                        id='visibility-radio-1'
                        value='public'
                        onChange={(e) => setVisibility('public')}
                        variant='secondary'
                        className={styles.radioSelectOption}
                    >
                        Public
                    </ToggleButton>
                    <ToggleButton
                        id='visibility-radio-2'
                        value='friends'
                        onChange={(e) => setVisibility('friends')}
                        variant='secondary'
                        className={styles.radioSelectOption}
                    >
                        Friends
                    </ToggleButton>
                    <ToggleButton
                        id='visibility-radio-3'
                        value='unlisted'
                        onChange={(e) => setVisibility('unlisted')}
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
                    isInvalid={!!errors.title}
                    className={styles.formControl}
                />
                <Form.Control.Feedback type='invalid'>
                    {errors.title}
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
                    isInvalid={!!errors.description}
                    className={styles.formControl}
                />
                <Form.Control.Feedback type='invalid'>
                    {errors.description}
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
                    isInvalid={!!errors.content}
                    className={styles.formControl}
                />
                <Form.Control.Feedback type='invalid'>
                    {errors.content}
                </Form.Control.Feedback>
            </Form.Group>
            {/** Post Button */}
            <Button type='submit' className={styles.submitButton}>
                Submit
            </Button>
        </Form>
    );
}

export default TextPostForm;