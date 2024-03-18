import { useEffect, useRef, useState } from "react";
import { ListGroup, Image, Col, Row, Alert } from "react-bootstrap";
import styles from "./CommentSection.module.css";
import { baseURL } from "../../constants";
import { getUserId } from "../../utils/auth";
import { apiRequest } from "../../utils/request";

interface CommentSectionProps {
    postId: string
}

interface CommentProps {
    authorUrl: string,
    authorName: string,
    profileImg: string,
    comment: string,
    date: string
}

const CommentSection: React.FC<CommentSectionProps> = (props: CommentSectionProps) => {
    const { postId } = props;
    const [comments, setComments] = useState<CommentProps[]>([{
        authorUrl: "/",
        authorName: "Hello World",
        profileImg: "https://th.bing.com/th/id/R.84a17e40341b39efb41844322681df18?rik=Dnof5ZF8%2fyLpFA&pid=ImgRaw&r=0",
        comment: "Butterfly Day lorem ipsumijwiopefjoipjowin ejfioajosijd jwiejfpojqskd joijaOInsdjvn jifajoiwjeopfj ijiojiojewoifjijj jijojewfpoijojjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiioooooooooooooooooooooooooooooooooooooooooooooooooppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
        date: "Today" 
    },
    {
        authorUrl: "/",
        authorName: "New Person",
        profileImg: "https://zvelo.com/wp-content/uploads/2018/11/anatomy-of-a-full-path-url-hostname-tld-path-protocol.jpg",
        comment: "So tired T~T",
        date: "Yesterday" 
    }]);
    const [responseMessage, setResponseMessage] = useState<string>("");
    const pageSize = 5;
    const currentPage = useRef(1);

    {/** Comment section */}
    return (
        <>
            {/** Alert for request errors */}
            {!!responseMessage ? (
                <Alert variant='danger' data-bs-theme='dark' dismissible>
                    <Alert.Heading>An Error Occured When Sending Your Request To The Server</Alert.Heading>
                    <hr />
                    <p>{responseMessage || 'An error occured'}</p>
                </Alert>
            ) : null}
            {/** Comments section */}
            <ListGroup>
                {comments.map((comment) => (
                    <ListGroup.Item>
                        <Row>
                            <Col className={styles.commentImageContainer}>
                                <Image src={comment.profileImg} roundedCircle width={50} height={50} />
                            </Col>
                            <Col className={styles.commentInfoContainer}>
                                <a href={comment.authorUrl} className={styles.author}>{comment.authorName}</a>
                                <p className={styles.date}>{comment.date}</p>
                                <p className={styles.comment}>{comment.comment}</p>
                            </Col>
                        </Row>
                    </ListGroup.Item>
                ))}
            </ListGroup>

        </>
    );
}

export default CommentSection;