import React, { useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';
import { InboxResponse, PaginatedAPI } from '../../api/types';
import { getInboxMessages } from '../../api/inbox'; 
import { getUserId } from '../../utils/auth';
import { ReactComponent as Allow } from 'bootstrap-icons/icons/check-lg.svg';
import { ReactComponent as Deny } from 'bootstrap-icons/icons/x-lg.svg';
import styles from './Inbox.module.css';
import { apiDeleteFollower, apiPutFollower } from '../../api/following';
import { apiClearInbox } from '../../api/inbox';
import { Author } from '../../api/types';

const Inbox = () => {

    const [inboxMessages, setInboxMessages] = useState<any[]>([]);
    const [pageNo, setPageNo] = useState<number>(1);
    const [pageSize, setPageSize] = useState<number>(10);
    const curAuthorId = getUserId();
    
    /** Gets the user's inbox */
    useEffect(() => {
        const getMessages = async () => {
            try {
                getInboxMessages(curAuthorId, pageNo, pageSize)
                    .then(res => {
                        setInboxMessages(res.items);
                        console.log(res.items); });
            } catch (error) {
                console.log("failed to fetch inbox:", error);
            };
        };
        getMessages();
    }, []);

    /** Function for rendering post notification */
    const renderPostCard = (message: any, idx: number) => {
        return (
            <Card key={message+idx} className="mb-2">
                <Card.Header>{message.author.displayName} just posted!</Card.Header>
                <Card.Body>
                    <Card.Text>Preview: {message.description}</Card.Text> 
                </Card.Body>
            </Card>
        );
    }

    /** Function for rendering follow request */
    const renderRequestCard = (message: any, idx: number) => {

        /** Function for handling acceptance of follow request */
        const followAccept = (author: Author, target_author: Author) => {
            apiPutFollower(author.id, target_author.id, target_author.host); // put follower on remote 
            apiPutFollower(author.id, target_author.id, author.host);        // put follower on local
            setInboxMessages(prevMessages => prevMessages.filter((_, index) => index !== idx)); 
        }

        /** Function for handling rejection of follow request */
        const followReject = (author_id: string, target_author_id: string) => {
            // TODO: delete follow request 
            setInboxMessages(prevMessages => prevMessages.filter((_, index) => index !== idx)); 
        }

        /** Follow request card */
        return (
            <Card key={message+idx} className="mb-2">
                <Card.Header>Follow Request</Card.Header>
                <Card.Body>
                    {/** Follow request information */}
                    <Card.Text>type: {message.type}</Card.Text>
                    <Card.Text>from: {message.author.displayName}</Card.Text>
                    <Card.Text>to: {message.target_author.displayName}</Card.Text>
                    {/** Accept and Reject buttons */}
                    <div className={styles.postButtons}>
                        <Allow 
                            className={`${styles.postButton} ${styles.postShare}`} 
                            onClick={() => {followAccept(message.author, message.target_author)}} 
                        />
                        <Deny className={`${styles.postButton} ${styles.postLike}`}
                            onClick={() => {followReject(message.author.id, message.target_author.id)}} 
                        />
                    </div> 
                </Card.Body>
            </Card>
        );    
    }
    
    /** Function for rendering like notification */
    const renderLikeCard = (message: any, idx: number) => {
        // TODO: Implement 
        return (
            <Card key={message+idx} className="mb-2">
                <Card.Header>Like</Card.Header>
                <Card.Body>
                    <Card.Text>{message.summary}</Card.Text> 
                </Card.Body>
            </Card>
        );
    }
    
    /** Function for rendering comment like notification */
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

    /** Function for rendering an inbox card */
    const renderCard = (message:any, idx: number) => {
        switch (message.type) {
            case 'Like':
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

    /** Inbox */
    return (
        <div className={styles.cardContainer}>
            {/** Render inbox cards */}
            <div className={styles.cardContainer}>
                {inboxMessages.map((message, idx) => (
                    renderCard(message, idx)
                ))}
            </div>
            {(inboxMessages.length === 0)
                ? "Empty..."
                : <button className="btn btn-warning" onClick={async () => {
                    apiClearInbox(curAuthorId);
                    setInboxMessages([]);
                }}>
                    Clear Inbox
                </button>
            } 
        </div>
    );
};

export default Inbox;
