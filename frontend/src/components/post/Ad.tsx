import React, { useState, useRef } from 'react';
import Markdown from 'react-markdown';
import styles from './Post.module.css';
import { ContentType, Ad as AdTy } from '../../api/types'
import { Colors, baseURL, publicDir } from "../../constants";
import { getUserId } from '../../utils/auth';
import { apiCreatePostLike } from '../../api/likes';
import { Row, Col, Offcanvas, Overlay, Tooltip } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Ad: React.FC<AdTy> = props => {
    // Determine post content format
    let content;
    switch (props.contentType) {
        case ContentType.MARKDOWN:
            content = <Markdown>{props.content}</Markdown>;
            break;
        case ContentType.PLAIN:
            content = <span>{props.content}</span>;
            break;
        case ContentType.APPLICATION_BASE64:
        case ContentType.PNG_BASE64:
        case ContentType.JPEG_BASE64:
            content = <img style={{ maxWidth: "100%" }} src={props.content} alt="Image Post" />;
            break;
        default:
            content = <span>{props.content}</span>;
            break;
    }

    /** Ad */
    return (
        <div className={`${styles.postContainer} ${styles.ad}`}>
            {/* Header */}
            <Row className={styles.postHeader}>
                {/* Ad info */}
                <Col className={"flex-grow-1"}>
                    <div className={styles.postInfo}>
                        {/* Company */}
                        <span className={styles.postAuthor}>
                            {props.company}
                        </span>
                        {/* Sub info */}
                        <div className={styles.postSubInfo}>
                            {/* Debug Domain */}
                            <div className={styles.postSubInfoItem} style={{ fontStyle: "italics", fontWeight: "bold" }}>Sponsored Ad</div>
                        </div>
                    </div>
                </Col>
            </Row>
            {/* Body */}
            <div className={styles.postBody}>
                {/* Title */}
                <div className={styles.postTitle}>{props.title}</div>
                <div className={styles.postDescr}>{props.description}</div>
                {/* Content */}
                <div className={styles.postContent}>{content}</div>
            </div>
        </div>
    );
}

export default Ad;
