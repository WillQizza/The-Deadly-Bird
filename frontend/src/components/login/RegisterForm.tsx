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

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (validateForm()) {
            console.log("Submit!", baseURL);
            
            const formData = new URLSearchParams({
                username: username,
                password: password
            }).toString()
            
            const response = await apiRequest(`${baseURL}/api/register/`, {
                method:"POST",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });
            
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

    const validateForm = () => {
        let isValid = true;
        const newErrors: { [key: string]: string } = {};

        if (!username) {
            isValid = false;
            newErrors.username = "Username is required";
        } if (!email) {
            isValid = false;
            newErrors.email = "Email is required";
        } if (!password) {
            isValid = false;
            newErrors.password = "Password is required";
        } if (password !== confirmPassword) {
            isValid = false;
            newErrors.confirmPassword = "Passwords do not match";
        }

        setErrors(newErrors);
        return isValid;
    };

    return (
        <div className={styles.formContainer}>
            {registerMessage && (
                <div className="alert alert-warning" role="alert">
                    {registerMessage}
                </div>
            )}
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formBasicEmail" className={styles.formGroup}>
                    <Form.Label className={styles.formLabel}>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.username}
                    </Form.Control.Feedback>
                </Form.Group>

                <Form.Group controlId="formBasicEmail" className={styles.formGroup}>
                    <Form.Label className={styles.formLabel}>Email</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className={styles.formControl}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.email}
                    </Form.Control.Feedback>
                </Form.Group>

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