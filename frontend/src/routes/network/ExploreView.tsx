import React, { useState, useEffect } from "react";
import { Author } from "../../api/types";
import { getAuthors } from "../../api/authors";
import styles from "./ExploreView.module.css";
import AuthorCarousel from "./AuthorCarousel";


const ExploreView: React.FC = () => {
    
    const [exploreAuthors, setExploreAuthors] = useState<Author[]>([]);
    const [curPage, setCurPage] = useState<number>(1);
    const [isNextPageAvailable, setIsNextPageAvailable] = useState<boolean>(false);
    const [pageSize, setPageSize] = useState<number>(5);

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
            {/* <div id={styles.NetworkExploreHeader}>
                Explore Local Authors
            </div> */}
            <div className={styles.carouselContainer}>
                <div className={`${styles.pageButton} ${styles.prevButton}`} onClick={() => curPage > 1 && setCurPage(curPage - 1)}>
                    &lt;
                </div>
                <AuthorCarousel authors={exploreAuthors} />
                <div className={`${styles.pageButton} ${styles.nextButton}`} onClick={() => isNextPageAvailable && setCurPage(curPage + 1)}>
                    &gt;
                </div>
            </div>
            <div className={styles.pageNo}>
                Page {curPage}  
            </div>
        </div>
    );
};

export default ExploreView;
