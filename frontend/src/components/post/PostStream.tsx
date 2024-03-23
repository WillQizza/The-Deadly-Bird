import React, { useEffect, useState, useRef } from 'react';
import styles from './PostStream.module.css';
import Post from './Post';
import { apiGetAuthorPosts, apiGetPost, apiGetPosts, APIPostStreamTy } from '../../api/posts';
import { apiGetPostLikes } from '../../api/likes';
import { getUserId } from '../../utils/auth';
import { PostsResponse } from '../../api/types';

export enum PostStreamTy {
    Public,
    Author,
    Following,
    Single,
}

export type PostStreamArgs = {
    type: PostStreamTy,
    authorID: string | null,
    postID: string | null,
}

const PostStream: React.FC<PostStreamArgs> = (props: PostStreamArgs) => {
    const [posts, setPosts] = useState<React.ReactElement[]>([]);
    const postRef = useRef<HTMLDivElement>(null);
    const currentPage = useRef(1);
    const failedToLoadPosts = useRef(0);
    const pageSize = 5;

    // function to generate posts (and wait until last post is reached to generate more)
    const generatePosts = async (reset?: boolean) => {
        let response: PostsResponse;
        if (props.type === PostStreamTy.Author && props.authorID) {   // Get profile posts
            response = await apiGetAuthorPosts(props.authorID, currentPage.current, pageSize);
        } else if (props.type === PostStreamTy.Public) {    // Get public posts
            response = await apiGetPosts(APIPostStreamTy.Public, currentPage.current, pageSize);
        } else if (props.type === PostStreamTy.Following) { // Get following posts
            response = await apiGetPosts(APIPostStreamTy.Following, currentPage.current, pageSize);
        } else if (props.type === PostStreamTy.Single && props.authorID && props.postID) { // Get single post
            let singleResponse = await apiGetPost(props.authorID, props.postID);
            if (singleResponse !== null) {
                response = {
                    type: "posts",
                    next: "",
                    prev: "",
                    items: [
                        singleResponse
                    ],
                }
            } else {
                response = {
                    type: "posts",
                    next: "",
                    prev: "",
                    items: [],
                }
            }
        } else {
            console.error(`Unknown post stream type: ${props.type}`);
            return;
        }

        if ('items' in response) {
            const newPosts = (await Promise.all(response.items.map(async (postResponse) => {
                try {
                    const likes = await apiGetPostLikes(postResponse.author.id, postResponse.id);
                    const isLikedByUs = !!likes.find(like => like.author.id === getUserId());
                    return (
                        <Post
                            key={`${postResponse.author.id}/${postResponse.id}`}
                            {...postResponse} 
                            likes={likes.length}
                            isLiked={isLikedByUs}
                            refreshStream={() => {
                                currentPage.current = 1;
                                generatePosts(true);
                            }}
                        />
                    );
                } catch (error) {
                    failedToLoadPosts.current = failedToLoadPosts.current + 1;
                    console.error(error);
                    return null;
                }
            }))).filter(post => post !== null) as any[];

            reset ? setPosts(newPosts) : setPosts([...posts, ...newPosts]);
        }
    }

    // generate initial posts
    useEffect(() => {
        generatePosts(true);
    }, []);

    // generate new posts while scrolling
    useEffect(() => {
        // check if posts need generated
        if (Math.floor((posts.length + failedToLoadPosts.current) / pageSize) < currentPage.current) {
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
    }, [posts, failedToLoadPosts])

    /** Post stream */
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
