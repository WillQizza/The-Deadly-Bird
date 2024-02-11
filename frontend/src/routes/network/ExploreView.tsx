import React, { useState, useEffect } from "react";
import { Author } from "../../api/types";
import { getAuthors } from "../../api/authors";
import styles from "./ExploreView.module.css";

const ExploreView: React.FC = () => {
    
    const [exploreAuthors, setExploreAuthors] = useState<Author[]>([]);
    const [curPage, setCurPage] = useState<number>(1);
    const [isNextPageAvailable, setIsNextPageAvailable] = useState<boolean>(false);
    const [pageSize, setPageSize] = useState<number>(6);

    const fetchSetAuthors = async (page: number) => {
        const response = await getAuthors(page, pageSize);
        setExploreAuthors(response.results.items);
        setIsNextPageAvailable(response.results.items.length === pageSize);
    };

    useEffect(() => {
        fetchSetAuthors(curPage);
    }, [curPage]);


    const handlePrevPage = () => {
        if (curPage > 1) {
            setCurPage(curPage - 1);
        }
    };

    const handleNextPage = () => {
        if (isNextPageAvailable) {
            setCurPage(curPage + 1);
        }
    };

    const handleFollow = (authorId: string) => {
        console.log(`Following author with ID: ${authorId}`);
        // Implement follow functionality here
    };

    return ( 
        <div>
            <div id={styles.NetworkExploreHeader}>
                Some Local Authors you may Know
            </div>
            <div id={styles.NetworkContentContainer}>
                <div id={styles.AuthorCards}>
                    {exploreAuthors.map((author) => (
                        <div key={author.id} id={styles.AuthorCard}>
                            <img src={author.profileImage} alt={author.displayName} 
                                style={{width: 50, height: 50, borderRadius: '50%'}} />
                            <div>
                                <h2>{author.displayName}</h2>
                                <p>{author.host}</p>
                                <a href={author.url} className={styles.plainLink}>Profile</a> | 
                                <a href={author.github} className={styles.plainLink}>GitHub</a>
                                <button 
                                    className="btn btn-primary"
                                    onClick={() => handleFollow(author.id)}
                                    style={{ width: '100%', marginTop: '10px' }}
                                >
                                    Follow
                                </button> 
                            </div>
                        </div>
                    ))}
                </div>        
                <div id={styles.PageButtons}>
                    <button className={styles.pageButton} onClick={handlePrevPage} disabled={curPage===1}>
                        Prev
                    </button>
                    Page {curPage}
                    <button className={styles.pageButton} onClick={handleNextPage} disabled={!isNextPageAvailable}>
                        Next
                    </button>
                </div>
            </div>
             
        </div>
    );
};

export default ExploreView;
