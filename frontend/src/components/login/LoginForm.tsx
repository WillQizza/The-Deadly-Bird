import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import styles from "./LoginForm.module.css";

const LoginForm: React.FC = () => {
    
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        console.log('Logging in with:', username, password);
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