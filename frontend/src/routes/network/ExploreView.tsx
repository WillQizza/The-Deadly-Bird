import React, { useState, useEffect } from "react";
import { Author } from "../../api/types";
import { apiGetAuthors } from "../../api/authors";
import styles from "./ExploreView.module.css";
import AuthorCarousel from "./AuthorCarousel";
import { apiGetFollowing } from "../../api/following";
import { getUserId } from "../../utils/auth";

interface ExploreViewProps {
    viewType: string
};

const ExploreView: React.FC<ExploreViewProps> = ({viewType}) => {
    
    const [exploreAuthors, setExploreAuthors] = useState<Author[]>([]);
    const [isNextPageAvailable, setIsNextPageAvailable] = useState<boolean>(false);
    const [curPage, setCurPage] = useState<number>(1);
    const [pageSize, setPageSize] = useState<number>(5);

    /** Function to fetch authors for a specified page number */
    const fetchSetAuthors = async (page: number) => {
        const response = await apiGetAuthors(page, pageSize);
        setExploreAuthors(response.items);
        setIsNextPageAvailable(response.items.length === pageSize);
    };

    /** Gets authors based on view type */
    useEffect(() => {
        if (viewType === "local") {
            fetchSetAuthors(curPage);
        } else if (viewType == "remote") {
            setExploreAuthors([]);
        }
    }, [curPage]);

    /** Explore view */
    return (
        <div className={styles.exploreViewContainer}>
            {/* {exploreAuthors.length === 0
                ? "None Found"
                : "Found" 
            } */}
            {/** Page navigation */}
            <div className={styles.pageNo}>
                <div className={`${styles.pageButton} ${styles.prevButton}`} onClick={() => curPage > 1 && setCurPage(curPage - 1)}>
                    &lt;
                </div> 
                Page {curPage} 
                <div className={`${styles.pageButton} ${styles.nextButton}`} onClick={() => isNextPageAvailable && setCurPage(curPage + 1)}>
                    &gt;
                </div>
            </div>
            {/** Authors */}
            <div className={styles.carouselContainer}>
                <AuthorCarousel authors={exploreAuthors} /> 
            </div>
        </div>
    );
};

export default ExploreView;
