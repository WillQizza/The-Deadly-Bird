import React from 'react';
import styles from './PostCreationPage.module.css';
import { Tab, Tabs } from 'react-bootstrap';
import TextPostForm from '../../components/post/TextPostForm';
import ImagePostForm from '../../components/post/ImagePostForm';
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
                        <TextPostForm />
                    </Tab>
                    <Tab eventKey='image' title='Image'>
                        <ImagePostForm />
                    </Tab>
                </Tabs>
            </div>
        </Page>
    );
}

export default PostCreationPage;