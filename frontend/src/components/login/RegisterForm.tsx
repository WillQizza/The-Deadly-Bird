import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import styles from "./RegisterForm.module.css";
import { baseURL } from "../../constants";
import { apiRequest } from '../../utils/request';

type RegisterProps = {
    showLogin: boolean;
    setShowLogin: (show: boolean) => void;
};

const RegisterForm: React.FC<RegisterProps> = (props: RegisterProps) => {
    
    const [username, setUsername] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [confirmPassword, setConfirmPassword] = useState<string>('');
    const [errors, setErrors] = useState<{ [key: string]: string }>({});
    const [registerMessage, setRegisterMessage] = useState<string>('');

    /** Function for handling form submission */
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (validateForm()) {
            console.log("Submit!", baseURL);
            
            // send registration request
            const formData = new URLSearchParams({
                username: username,
                email: email,
                password: password
            }).toString()
            
            const response = await apiRequest(`${baseURL}/api/register/`, {
                method:"POST",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });
            
            // handle response
            setErrors({});
            if (response.status === 201) {
                props.setShowLogin(true);
            } else if (response.status === 409 || response.status === 400) {
                const data = await response.json();
                setRegisterMessage(data.message);
                console.log(registerMessage);   
            }
        }
    };

    /** Function to validate form input */
    const validateForm = () => {
        let isValid = true;
        const newErrors: { [key: string]: string } = {};

        if (!username) {
            isValid = false;
            newErrors.username = "Username is required";
        }
        if (username.length > 150) {
            isValid = false;
            newErrors.username = "Username is too long (150 characters maximum)";
        }
        if (!email) {
            isValid = false;
            newErrors.email = "Email is required";
        }
        if (email.length > 254) {
            isValid = false;
            newErrors.email = "Email is too long (254 characters maximum)";
        }
        if (!password) {
            isValid = false;
            newErrors.password = "Password is required";
        }
        if (password !== confirmPassword) {
            isValid = false;
            newErrors.confirmPassword = "Passwords do not match";
        }

        setErrors(newErrors);
        return isValid;
    };

    /** Registration page */
    return (
        <div className={styles.formContainer}>
            {/** Alert warning for request errors */}
            {registerMessage && (
                <div className="alert alert-warning" role="alert">
                    {registerMessage}
                </div>
            )}
            {/** Form */}
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formBasicEmail" className={styles.formGroup}>
                    {/** Username input */}
                    <Form.Label className={styles.formLabel}>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        isInvalid={!!errors.username}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.username}
                    </Form.Control.Feedback>
                </Form.Group>

                {/** Email input */}
                <Form.Group controlId="formBasicEmail" className={styles.formGroup}>
                    <Form.Label className={styles.formLabel}>Email</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        isInvalid={!!errors.email}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.email}
                    </Form.Control.Feedback>
                </Form.Group>

                {/** Password input */}
                <Form.Group controlId="formBasicPassword" className={styles.formGroup}>
                    <Form.Label className={styles.formLabel}>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        isInvalid={!!errors.password}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.password}
                    </Form.Control.Feedback>
                </Form.Group>
                {/** Confirm password input */}
                <Form.Group controlId="formConfirmPassword" className={styles.formGroup}>
                    <Form.Label className={styles.formLabel}>Confirm Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Confirm Password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        isInvalid={!!errors.confirmPassword}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.confirmPassword}
                    </Form.Control.Feedback>
                </Form.Group>
 
                {/** Sign up button */}
                <Button variant="primary" type="submit"
                    className={styles.btnPrimary}
                >
                    Sign Up
                </Button>
            </Form>
        </div>
    );
};

export default RegisterForm;