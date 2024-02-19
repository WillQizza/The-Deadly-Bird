import React, { useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';
import { InboxResponse, PaginatedAPI } from '../../api/types';
import { getInboxMessages } from '../../api/inbox'; 
import { useParams } from 'react-router-dom';

const Inbox = () => {

    const [inboxMessages, setInboxMessages] = useState<any[]>([]);
    const [pageNo, setPageNo] = useState<number>(1);
    const [pageSize, setPageSize] = useState<number>(10);
    const params = useParams();
    const userId = params["id"] ? String(params["id"]) : '';
 
    useEffect(() => {
        const getMessages = async () => {
            try {
                const res: InboxResponse = await getInboxMessages(userId, pageNo, pageSize);
                setInboxMessages(res.items);
            } catch (error) {
                console.log("failed to fetch inbox:", error);
            };
        };
        getMessages();
        console.log(inboxMessages, inboxMessages.length);
    }, []);

    return (
        <div style={{ maxHeight: '100%', overflowY: 'auto' }}>
            {inboxMessages.map((message, idx) => (
                <Card key={message+idx} className="mb-2">
                    <Card.Header>Follow Request</Card.Header>
                    <Card.Body>
                        <Card.Text>{message.type}</Card.Text>
                        <Card.Text> from: {message.author.displayName}</Card.Text>
                        <Card.Text> to: {message.target_author.displayName}</Card.Text>
                    </Card.Body>
                </Card>
            ))}
        </div>
    );
};

export default Inbox;
