import React from 'react';

import styles from "./HomePage.module.css";
import Page from '../../components/layout/Page';
import PostStream, { PostStreamTy } from '../../components/post/PostStream';
import Nav from 'react-bootstrap/Nav'
import Tab from 'react-bootstrap/Tab'

const HomePage: React.FC = () => {
    
    return ( 
        <Page selected="Home" overflowScrollOff={true}>
            <div className={styles.tabs}>
                <Tab.Container defaultActiveKey="Following">
                    <Nav variant="pills"justify={true}>
                        <Nav.Item>
                            <Nav.Link eventKey="Following">Following</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="Public">Public</Nav.Link>
                        </Nav.Item>
                    </Nav>
                    <Tab.Content className={styles.tabContent}>
                        <Tab.Pane eventKey="Following">
                            <PostStream type={PostStreamTy.Following} id={null} />
                        </Tab.Pane>
                        <Tab.Pane eventKey="Public">
                            <PostStream type={PostStreamTy.Public} id={null} />
                        </Tab.Pane>
                    </Tab.Content>
                </Tab.Container>
            </div>
        </Page>
    );
};

export default HomePage;
