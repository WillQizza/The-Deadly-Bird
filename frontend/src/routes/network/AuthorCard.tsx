import React, { useEffect } from 'react';
import styles from './AuthorCard.module.css';
import { Author } from '../../api/types';
import { Card } from 'react-bootstrap';
import { extractAuthorIdFromApi } from '../../api/utils';
import { useNavigate } from 'react-router-dom';

const AuthorCard: React.FC<{author: Author, host: string}> = ({author, host}) => {
    
    useEffect(() => {
        console.log(author.host, host);
    }, []);
    
    const navigate = useNavigate();
    const handleCardClick = (authorId: string) => {
        navigate(`/profile/${authorId}`);
    };

    let subdomain = author.host.split(".")[0];
    if (subdomain.indexOf("//") === -1) {
        subdomain = "Invalid Host URL";
    } else {
        subdomain = subdomain.substring(subdomain.indexOf("//") + 2);
    }

    return (
        <div className={styles.author_card}
            onClick={() => handleCardClick(extractAuthorIdFromApi(author.id))}
        > 
            <img src={author.profileImage || 'https://via.placeholder.com/150'} 
                 alt="Profile" 
            />
            <div className={styles.displayName}> 
                {author.displayName}
            </div>

            <div className={styles.remote}
                style={{ 
                    backgroundColor: !author.host.includes(host) ? "rgb(19, 211, 211)" : "rgb(11, 36, 127)",
                }}
            >
                {!author.host.includes(host) ? "Remote" : "Local"}
            </div>

            <div className={styles.remote}
                style={{ 
                    backgroundColor: "rgb(123, 136, 136)"
                }}>
                {subdomain}
            </div>
        </div>
    );
}

export default AuthorCard;