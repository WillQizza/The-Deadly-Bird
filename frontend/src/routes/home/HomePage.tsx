import React, { useState, useRef } from 'react';
import styles from "./HomePage.module.css";
import Page from '../../components/layout/Page';
import PostStream, { PostStreamTy } from '../../components/post/PostStream';
import Nav from 'react-bootstrap/Nav'
import Tab from 'react-bootstrap/Tab'

const HomePage: React.FC = () => {
    const tabContent = useRef<HTMLDivElement>(null);
    const [activeKey, setActiveKey] = useState('Following');

    const resetScroll = () => {
        if (tabContent.current) {
            tabContent.current.scrollTop = 0;
        }
    }

    const handleSelect = (eventKey: string | null) => {
        resetScroll();
        if (eventKey) {
            setActiveKey(eventKey);
        }
    }
    
    return ( 
        <Page selected="Home" overflowScrollOff={true}>
            <div className={styles.tabs}>
                <Tab.Container defaultActiveKey="Following">
                    <Nav className={styles.nav} variant="pills" justify={true} onSelect={handleSelect}>
                        <Nav.Item>
                            <Nav.Link eventKey="Following" className={`${styles.tab} ${activeKey === 'Following' ? styles.tabActive : styles.tabInactive}`}>Following</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="Public" className={`${styles.tab} ${activeKey === 'Public' ? styles.tabActive : styles.tabInactive}`}>Public</Nav.Link>
                        </Nav.Item>
                    </Nav>
                    <Tab.Content className={styles.tabContent} ref={tabContent}>
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
