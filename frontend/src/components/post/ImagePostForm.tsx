import { Alert, Button, Form, ToggleButton, ToggleButtonGroup } from 'react-bootstrap';
import styles from './PostForm.module.css';
import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { baseURL, publicDir } from '../../constants';

const ImagePostForm: React.FC = () => {
    const [title, setTitle] = useState<string>('');
    const [description, setDescription] = useState<string>('');
    const [image, setImage] = useState<string>(`${publicDir}/static/icons/image.svg`);
    const [visibility, setVisibility] = useState<string>('PUBLIC');
    const [formErrors, setFormErrors] = useState<{ [key: string]: string }>({});
    const [responseMessage, setResponseMessage] = useState<string>('');
    const fileInputRef = useRef<HTMLInputElement>(null);
    const navigate = useNavigate();

    /** function for handling form submission */
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
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
                {/** Visibility Select */}
                <ToggleButtonGroup
                    type='radio'
                    name='visibility-options'
                    defaultValue='PUBLIC'
                    className={styles.formGroup}
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
                    <div className={styles.imgUploadContainer}>
                        <div
                            className={styles.imgPreviewContainer}
                            onClick={(e) => {
                                if (fileInputRef && fileInputRef.current) {
                                    fileInputRef.current.click();
                                }
                            }}
                        >
                            <img src={image} alt='image-preview'/>
                        </div>
                        <Form.Control
                            type='file'
                            accept='.png, .jpg, .jpeg'
                            ref={fileInputRef}
                            onChange={(e) => {
                                if (e.target) {
                                    let target = e.target as HTMLInputElement;
                                    if (target.files && target.files[0]) {
                                        setImage(URL.createObjectURL(target.files[0]));
                                    }
                                }
                            }}
                        />
                    </div>
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

export default ImagePostForm;