import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Carousel, Card, Row, Col, Button } from 'react-bootstrap';
import { Author } from '../../api/types';
import styles from './AuthorCarousel.module.css';
import { getUserId } from '../../utils/auth';
import { apiFollowRequest } from '../../api/following';

const AuthorCarousel = ({authors}: {authors: Author[]}) => {
    const userId: string = getUserId().toString();

    /** Function for splitting an array into chunks of the given size */
    const chunk = (arr: any, size: number) =>
        Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
            arr.slice(i * size, i * size + size)
        );
    
    // variables
    const itemGroups = chunk(authors, 5);
    const navigate = useNavigate();

    /** Function handling when an author card is clicked */
    const handleCardClick = (authorId: string) => {
        navigate(`/profile/${authorId}`);
    };

    /** Author carousel */
    return (
        <div className={styles.carousel}>
            <Carousel indicators={false} controls={false} wrap={false}>
                {/** Rows containing author cards */}
                {itemGroups.map((group, index) => (
                    <Carousel.Item key={index}>
                        <Row>
                            {/** Row containing author cards */}
                            {group.map((author: Author, idx: number) => (
                                <Col key={idx}>
                                    {/** Author card */}
                                    <Card className={styles.card}>
                                        <Card.Img variant="top" src={author.profileImage || 'https://via.placeholder.com/150'} 
                                            onClick={() => handleCardClick(author.id)} 
                                        />
                                        <Card.Body>
                                            <div className={styles.cardDisplayname}>{author.displayName}</div>
                                            <div className="card-host">{author.host}</div> 
                                        </Card.Body>
                                    </Card>
                                </Col>
                            ))}
                        </Row>
                    </Carousel.Item>
                ))}
            </Carousel>
        </div>
    );
};

export default AuthorCarousel;