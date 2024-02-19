import React, { useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';
import { InboxResponse, PaginatedAPI } from '../../api/types';
import { getInboxMessages } from '../../api/inbox'; 
const Inbox = () => {

    const [inboxMessages, setInboxMessages] = useState<any[]>([]);
    const [pageNo, setPageNo] = useState<number>(0);

    useEffect(() => {
        const getMessages = async () => {
            try {
                const res: InboxResponse = await getInboxMessages(1, 1, 10);
                console.log(res);
                setInboxMessages(res.items);
                console.log(inboxMessages);
            } catch (error) {
                console.log("failed to fetch inbox:", error);
            };
        };
        getMessages();
    }, []);

    return (
        <div style={{ maxHeight: '100%', overflowY: 'auto' }}>
            {inboxMessages.map((message) => (
                <Card key={message} className="mb-2">
                    <Card.Header>Test</Card.Header>
                    <Card.Body>
                        <Card.Text>Body</Card.Text>
                    </Card.Body>
                </Card>
            ))}
        </div>
    );
};

export default Inbox;
