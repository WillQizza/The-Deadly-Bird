import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { baseURL } from '../../constants';
import styles from "./LoginForm.module.css";
import { useNavigate } from 'react-router-dom';
import { setUserId } from '../../utils/auth';
import { apiRequest } from '../../utils/request';

const LoginForm: React.FC = () => {
    
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [loginMessage, setLoginMessage] = useState<string>('');
    const [errors, setErrors] = useState<{ [key: string]: string }>({});
    const navigate = useNavigate();
 
    /** Function for handling form submission */
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (validateForm()) {
            // send login request
            const formData = new URLSearchParams({
                username: username,
                password: password
            }).toString()
            
            const response = await apiRequest(`${baseURL}/api/login/`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });
            
            // handle response
            if (response.ok) {
                const userId = (await response.json()).id;
                setUserId(userId);
                navigate('/home');
            } else if (response.status === 400 || response.status === 401) {
                const data = await response.json();
                setLoginMessage(data.message);
                console.log(loginMessage);
            }
        }
    };

    /** Function for validating form input */
    const validateForm = () => {
        let isValid = true;
        const newErrors: { [key: string]: string } = {};

        if (!username) {
            isValid = false;
            newErrors.username = "Username is required";
        } if (!password) {
            isValid = false;
            newErrors.password = "Password is required";
        }

        setErrors(newErrors);
        return isValid;
    };

    /** Login form */
    return (
        <div className={styles.loginFormContainer}>
            {/** Alert warning for request errors */}
            {loginMessage && (
                <div className="alert alert-warning" role="alert">
                    {loginMessage}
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

                {/** Password input */}
                <Form.Group controlId="formBasicPassword"
                    style={{marginTop: '10px'}}
                    className={styles.formGroup}
                >
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

                {/** Login button */}
                <Button variant="primary" type="submit"
                    style={{marginTop: '20px'}}
                    className={styles.btnPrimary}
                >
                    Login
                </Button>


            </Form>
        </div>
    );
};

export default LoginForm;
