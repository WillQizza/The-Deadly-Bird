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
                const res: InboxResponse = await getInboxMessages('1', pageNo, pageSize);
                console.log(res);
                setInboxMessages(res.items);
            } catch (error) {
                console.log("failed to fetch inbox:", error);
            };
        };
        getMessages();
        console.log(inboxMessages);
    }, []);

    return (
        <div style={{ maxHeight: '100%', overflowY: 'auto' }}>
            {/* {inboxMessages.map((message) => (
                <Card key={message} className="mb-2">
                    <Card.Header>Test</Card.Header>
                    <Card.Body>
                        <Card.Text>Body</Card.Text>
                    </Card.Body>
                </Card>
            ))} */}
        </div>
    );
};

export default Inbox;
