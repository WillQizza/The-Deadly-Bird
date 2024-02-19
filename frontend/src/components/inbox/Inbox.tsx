import React, { useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';
import { InboxResponse, PaginatedAPI } from '../../api/types';
import { getInboxMessages } from '../../api/inbox'; 
import { getUserId } from '../../utils/auth';
import { ReactComponent as Allow } from 'bootstrap-icons/icons/check-lg.svg';
import { ReactComponent as Deny } from 'bootstrap-icons/icons/x-lg.svg';
import styles from './Inbox.module.css';
import { apiDeleteFollower, apiPutFollower } from '../../api/following';

const Inbox = () => {

    const [inboxMessages, setInboxMessages] = useState<any[]>([]);
    const [pageNo, setPageNo] = useState<number>(1);
    const [pageSize, setPageSize] = useState<number>(10);
    const curAuthorId = getUserId().toString();
    
    useEffect(() => {
        const getMessages = async () => {
            try {
                getInboxMessages(curAuthorId, pageNo, pageSize)
                    .then(res => {
                        setInboxMessages(res.items);
                        console.log(res.items);
                    });
            } catch (error) {
                console.log("failed to fetch inbox:", error);
            };
        };
        getMessages();
    }, []);

    
    const renderPostCard = (message: any, idx: number) => {
        // TODO: Implement 
        return (
            <Card key={message+idx} className="mb-2">
                <Card.Header>Follow Request</Card.Header>
                <Card.Body>
                    <Card.Text>Liked your post!</Card.Text> 
                </Card.Body>
            </Card>
        );
    }

    const renderRequestCard = (message: any, idx: number) => {

        const followAccept = (author_id: string, target_author_id: string) => {
            apiPutFollower(target_author_id, author_id);
            setInboxMessages(prevMessages => prevMessages.filter((_, index) => index !== idx)); 
        }

        const followReject = (author_id: string, target_author_id: string) => {
            // TODO: delete follow request 
            setInboxMessages(prevMessages => prevMessages.filter((_, index) => index !== idx)); 
        }

        return (
            <Card key={message+idx} className="mb-2">
                <Card.Header>Follow Request</Card.Header>
                <Card.Body>
                    <Card.Text>type: {message.type}</Card.Text>
                    <Card.Text>from: {message.author.displayName}</Card.Text>
                    <Card.Text>to: {message.target_author.displayName}</Card.Text>
                    <div className={styles.postButtons}>
                        <Allow 
                            className={`${styles.postButton} ${styles.postShare}`} 
                            onClick={() => {followAccept(message.author.id, message.target_author.id)}} 
                        />
                        <Deny className={`${styles.postButton} ${styles.postLike}`}
                            onClick={() => {followReject(message.author.id, message.target_author.id)}} 
                        />
                    </div> 
                </Card.Body>
            </Card>
        );    
    }
    
    const renderLikeCard = (message: any, idx: number) => {
        // TODO: Implement 
        return (
            <Card key={message+idx} className="mb-2">
                <Card.Header>Follow Request</Card.Header>
                <Card.Body>
                    <Card.Text>Liked your post!</Card.Text> 
                </Card.Body>
            </Card>
        );
    }
    
    const renderCommentCard = (message: any, idx: number) => {
        // TODO: Implement 
        return (
            <Card key={message+idx} className="mb-2">
                <Card.Header>Follow Request</Card.Header>
                <Card.Body>
                    <Card.Text>Liked your post!</Card.Text> 
                </Card.Body>
            </Card>
        );
    }

    const renderCard = (message:any, idx: number) => {
        console.log("type:", message.type); 
        switch (message.type) {
            case 'like':
                return renderLikeCard(message, idx);
            case 'comment':
                return renderCommentCard(message, idx);
            case 'follow_request':
                return renderRequestCard(message, idx);
            case 'post':
                return renderPostCard(message, idx);
            default:
                return null;
        }
    };


    return (
        <div style={{ maxHeight: '100%', overflowY: 'auto' }}>
            {inboxMessages.map((message, idx) => (
                renderCard(message, idx)
            ))}
        </div>
    );
};

export default Inbox;
