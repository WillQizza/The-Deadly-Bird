import styles from './FormTextbox.module.css'
import { Form } from 'react-bootstrap';

interface FormTextboxProps {
    label: string,
    placeholder: string,
    formErrors: { [key: string]: string },
    formErrorKey: string,
    value: string,
    setValue: React.Dispatch<React.SetStateAction<string>>,
    textarea?: boolean
}

const FormTextbox: React.FC<FormTextboxProps> = (props: FormTextboxProps) => {
    const {
        label,
        placeholder,
        formErrors,
        formErrorKey,
        value,
        setValue,
        textarea = false
    } = props;

    /** Form textbox */
    return (
        <>
            <Form.Group className={styles.formGroup}>
                {/** Label */}
                <Form.Label className={styles.formLabel}>
                    {label}
                </Form.Label>
                {/** Input */}
                <Form.Control
                    type='text'
                    as={ textarea ? 'textarea' : 'input' }
                    placeholder={placeholder}
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    isInvalid={!!formErrors[formErrorKey]}
                    className={styles.formControl}
                />
                {/** Error message */}
                <Form.Control.Feedback type='invalid'>
                    {formErrors[formErrorKey]}
                </Form.Control.Feedback>
            </Form.Group>
        </>
    );
}

export default FormTextbox;