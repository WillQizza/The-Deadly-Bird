import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { baseURL } from '../../constants';
import styles from "./LoginForm.module.css";

const LoginForm: React.FC = () => {
    
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
 
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        // TODO: copy the implementation of Register Form 

        if (username && password) {
            
            const formData = new URLSearchParams({
                username: username,
                password: password
            }).toString()
            
            const response = await fetch(`${baseURL}/api/login/`, {
                method:"POST",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });
            
            if (response.ok) {
                console.log("log in");
            } else if (response.status == 400 || response.status == 404) {
                // TODO: set error messages for user
                console.log(response.json());
            }
        }
    };
    return (
        <div className={styles.loginFormContainer}>
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
                </Form.Group>

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
                        className={styles.formControl}
                    />
                </Form.Group>

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