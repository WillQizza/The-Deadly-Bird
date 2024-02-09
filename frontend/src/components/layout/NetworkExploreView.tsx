import React, { useState, useEffect } from "react";
import { getAuthors, Author } from "../../api/authors";
import styles from "./NetworkExploreView.module.css";

const NetworkExploreView: React.FC = () => {
    
    const [exploreAuthors, setExploreAuthors] = useState<Author[]>([]);
    /*TODO add buttons for pagination and pass into */
    const [curPage, setCurPage] = useState<number>(1);
    
    const fetchSetAuthors = async (page: number, size: number) => {

        const response = await getAuthors(page, size);
        setExploreAuthors(response.results.items);
        console.log(exploreAuthors);
    }

    useEffect(() => {
        fetchSetAuthors(curPage, 100);
    }, []);

    return ( 
        <div id={styles.NetworkDiscoverViewContainer}>
            {exploreAuthors.map((author) => (
                <div key={author.id} className="authorItem">
                    <img src={author.profileImage} alt={author.displayName} style={{width: 50, height: 50, borderRadius: '50%'}} />
                    <div>
                        <h2>{author.displayName}</h2>
                        <p>{author.host}</p>
                        <a href={author.url}>Profile</a> | <a href={author.github}>GitHub</a>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default NetworkExploreView;
