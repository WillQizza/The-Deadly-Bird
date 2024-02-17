import styles from './PostCreationPage.module.css';
import React from 'react';
import { Tab, Tabs } from 'react-bootstrap';
import PostForm from '../../components/post/PostForm';
import Page from '../../components/layout/Page';

const PostCreationPage: React.FC = () => {
    return (
        <Page>
            <div className={styles.postCreationContentContainer}>
                <h1 className={styles.pageTitle}>Create a Post</h1>
                <Tabs
                    defaultActiveKey='text'
                    justify
                    data-bs-theme='dark'
                    className={styles.pageTabs}
                >
                    <Tab eventKey='text' title='Text'>
                        <PostForm />
                    </Tab>
                    <Tab eventKey='image' title='Image'>
                        <PostForm image={true} />
                    </Tab>
                </Tabs>
            </div>
        </Page>
    );
}

export default PostCreationPage;