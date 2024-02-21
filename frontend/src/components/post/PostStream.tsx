import React, { useEffect, useState, useRef } from 'react';
import styles from './PostStream.module.css';
import Post from './Post';
import { apiGetAuthorPosts } from '../../api/posts';

export enum PostStreamTy {
    Public,
    Author,
    Friend,
}

export type PostStreamArgs = {
    type: PostStreamTy,
    id: string | null,
}

const PostStream: React.FC<PostStreamArgs> = (props: PostStreamArgs) => {
    const [posts, setPosts] = useState<React.ReactElement[]>([])
    const postRef = useRef<HTMLDivElement>(null);
    const currentPage = useRef(1);
    const pageSize = 5;

    // function to add posts to current posts
    const addPosts = (newPosts: React.ReactElement[]) => {
        setPosts([...posts, ...newPosts]);
    };

    // function to generate posts (and wait until last post is reached to generate more)
    const generatePosts = () => {
        if (props.id === null) {
            return;
        }

        apiGetAuthorPosts(props.id, currentPage.current, pageSize)
            .then(async response => {
                const newPosts = response.items.map((postResponse, index) => {
                    // remove comments and commentsSrc fields from post response
                    // TODO: this will probably be needed when comments are implemented
                    const { comments, commentsSrc, ...post} = postResponse;
                    return <Post key={`${post.author.id}/${post.id}`} {...post} />;
                })
                addPosts(newPosts);
            });
    }

    // generate initial posts
    useEffect(() => {
        generatePosts();
    }, []);

    // generate new posts while scrolling
    useEffect(() => {
        // check if posts need generated
        if (Math.floor(posts.length / pageSize) < currentPage.current) {
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    currentPage.current++;
                    generatePosts();
                    observer.unobserve(entry.target);
                }
            });
        }, {
            root: null,
            threshold: 0,
        });

        // begin observe
        if (postRef.current) {
            observer.observe(postRef.current);
        }

        // cleanup function
        return () => {
            if (postRef.current) {
                observer.unobserve(postRef.current);
            }
        }
    }, [posts])

    return (
        <div className={styles.postStream}>
            {posts.map((post, index) => (
                <div className={styles.postStreamPostContainer} key={post.key} ref={index === posts.length - 1 ? postRef : null}>
                    {post}
                </div>
            ))}
        </div>
    )
}

export default PostStream
