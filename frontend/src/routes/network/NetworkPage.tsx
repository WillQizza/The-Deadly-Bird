import React, {useEffect, useState} from 'react';

import styles from "./NetworkPage.module.css";
import Page from '../../components/layout/Page';
import AuthorCard from './AuthorCard';
import { apiGetAuthors } from '../../api/authors';
import { Author } from '../../api/types';
import { apiGetHostname } from '../../api/host';

const NetworkPage: React.FC = () => {
    
    const [authors, setAuthors] = useState<Author[]>();
    const [curPage, setCurPage] = useState<number>(1);
    const [nextPageAvailable, setNextPageAvailable] = useState<boolean>(false);
    const [hostname, setHostname] = useState<string>("");

    const pageSize = 10;

    const fetchSetAuthors = async (page: number) => {
        const response = await apiGetAuthors(page, pageSize);    
        setAuthors(response.items);
        if (response.items && response.items.length === pageSize) {
            setNextPageAvailable(true);
        } else {
            setNextPageAvailable(false);
        }
    };

    const fetchHostname = async () => {
        const hostRes = await apiGetHostname();
        setHostname(hostRes.hostname.replace(/\/$/, ""));
    }

    useEffect(() => {
        fetchHostname();
        fetchSetAuthors(curPage);
    }, [curPage]);

    return (
        <Page selected="Network">
            <div className={styles.networkPageContainer}>
                <div className={styles.authorContainer}>

                    {authors?.map((author, index) => (
                        <div style={{ animationDelay: `${index * 50}ms`}}>
                            <AuthorCard author={author} host={hostname}></AuthorCard>
                        </div>
                    ))}
                </div>
            </div>
           <div className={styles.pagination}>
                
                <button onClick={() => {
                    if (curPage > 1) {
                        setCurPage(curPage - 1)
                    }
                }}>
                    {"\<"}
                </button>
                
                <span>Page: {curPage}</span>
                
                <button onClick={() => {
                    if (nextPageAvailable) {
                        setCurPage(curPage + 1)
                    }
                }}>
                    {"\>"}
                </button>
            </div>

        </Page>
    );
};

export default NetworkPage;