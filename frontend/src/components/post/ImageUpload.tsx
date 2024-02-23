import styles from './ImageUpload.module.css'
import { useRef, useState } from 'react';
import { Form } from "react-bootstrap";
import { publicDir } from '../../constants';

interface ImageUploadProps {
    formErrors: { [key: string]: string },
    setFormErrors: React.Dispatch<React.SetStateAction<{[key: string]: string;}>>,
    formErrorKey: string,
    valueRef: { current: string },
    typeRef: { current: string }
}

const fileToBase64 = async (file: File) => {
    const blob = new Uint8Array(await file.arrayBuffer());
    
    let result = "";
    for (let i = 0; i < blob.byteLength; i++) {
        result += String.fromCharCode(blob[i]);
    }
    return btoa(result);
};

const ImageUpload: React.FC<ImageUploadProps> = (props: ImageUploadProps) => {
    const {
        formErrors,
        setFormErrors,
        formErrorKey,
        valueRef,
        typeRef
    } = props;
    
    const placeholder = `${publicDir}/static/icons/image.svg`;
    const allowedTypes = new Set(['image/png;base64', 'image/jpeg;base64', 'application/base64']);
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
            reader.onload = async () => {
                if (reader.result) {
                    let newFormErrors = {...formErrors};
                    // parse result
                    const base64data = reader.result.toString();
                    let mediaType = base64data.slice(base64data.indexOf(':')+1,base64data.indexOf(','));
                    if (mediaType.startsWith('application/') && mediaType.endsWith('base64')) {
                        mediaType = 'application/base64';
                    }
                    // if image type is valid
                    if (allowedTypes.has(mediaType)) {
                        setImage(base64data);
                        valueRef.current = await fileToBase64(file);
                        typeRef.current = mediaType;
                        newFormErrors[formErrorKey] = '';
                    }
                    // if image type is invalid
                    else {
                        setImage(placeholder);
                        valueRef.current = '';
                        typeRef.current = 'text/plain';
                        newFormErrors[formErrorKey] = 'Invalid file type (.png, .jpg, .jpeg, or binary required)';
                    }
                    setFormErrors(newFormErrors);
                }
            };
            // handle file reading errors
            reader.onerror = (err) => {
                console.log(err);
                formErrors[formErrorKey] = 'Error reading the uploaded file';
                setFormErrors({...formErrors});
            };
        }
    }

    return (
        <>
            <Form.Group className={styles.formGroup}>
                <Form.Label className={styles.formLabel}>
                    Content
                </Form.Label>
                <div
                    className={styles.imgPreviewContainer}
                    onClick={(e) => {
                        if (fileInputRef && fileInputRef.current) {
                            fileInputRef.current.click();
                        }
                    }}
                >
                    <img src={image} alt='preview (unavailable)'/>
                </div>
                <Form.Control
                    type='file'
                    accept='.png, .jpg, .jpeg'
                    ref={fileInputRef}
                    onChange={handleUpload}
                    isInvalid={!!formErrors[formErrorKey]}
                />
                <Form.Control.Feedback type='invalid'>
                    {formErrors.content}
                </Form.Control.Feedback>
            </Form.Group>
        </>
    );
}

export default ImageUpload;