import styles from './ImageUpload.module.css'
import { useRef, useState } from 'react';
import { Form } from "react-bootstrap";
import { publicDir } from '../../constants';

interface ImageUploadProps {
    formErrors: { [key: string]: string },
    formErrorKey: string,
    valueRef: { current: string },
    typeRef: { current: string },
    placeholder?: string
}

const ImageUpload: React.FC<ImageUploadProps> = (props: ImageUploadProps) => {
    const {
        formErrors,
        formErrorKey,
        valueRef,
        typeRef,
        placeholder = `${publicDir}/static/icons/image.svg`
    } = props;

    const [image, setImage] = useState<string>(placeholder);
    const fileInputRef = useRef<HTMLInputElement>(null);

    /** function for handling file upload */
    const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            // read the file
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            // handle the result
            reader.onload = () => {
                if (reader.result) {
                    const base64data = reader.result.toString();
                    console.log(base64data);
                    setImage(base64data);
                    valueRef.current = base64data;
                }
            };
            reader.onerror = (err) => {
                console.log(err);
                formErrors[formErrorKey] = 'Error reading the uploaded file'
            };
        }
    }

    return (
        <>
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
                        onChange={handleUpload}
                        isInvalid={!!formErrors[formErrorKey]}
                    />
                </div>
                <Form.Control.Feedback type='invalid'>
                    {formErrors.content}
                </Form.Control.Feedback>
            </Form.Group>
        </>
    );
}

export default ImageUpload;