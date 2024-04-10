import React, { useEffect, useState, useRef } from 'react';
import styles from './PostStream.module.css';
import Post from './Post';
import Ad from "./Ad";
import { apiGetAuthorPosts, apiGetPost, apiGetPosts, APIPostStreamTy } from '../../api/posts';
import { apiGetPostLikes } from '../../api/likes';
import { getUserId } from '../../utils/auth';
import { PostsResponse, PostsStreamResponse } from '../../api/types';
import { extractAuthorIdFromApi } from '../../api/utils';
import { Link } from 'react-router-dom';

export enum PostStreamTy {
    Public,
    Author,
    Following,
    Single,
}

export type EmptyStreamMessageArgs = {
    type: PostStreamTy,
    authorID: string | null,
}

const EmptyStreamMessage: React.FC<EmptyStreamMessageArgs> = (props: EmptyStreamMessageArgs) => {
    return (
        <div className={styles.emptyMessageContainer}>
            {/* Message */}
            <div className={styles.emptyMessageTitle}>
                No posts here.
            </div>

            {/* Following stream */}
            {props.type === PostStreamTy.Following && <>
                <div>
                    Grow your feed by following new authors:
                </div>
                <Link to={"/network"}>Explore Authors</Link>
            </>}

            {/* Public stream */}
            {props.type === PostStreamTy.Public && <>
                <div>
                    No one has made any posts. Make a public post:
                </div>
                <Link to={"/post"}>New Post</Link>
            </>}

            {/* Author streams */}
            {/* This author */}
            {props.type === PostStreamTy.Author && props.authorID !== null && extractAuthorIdFromApi(props.authorID) === getUserId() && <>
                <div>
                    You have not made any posts. Make a post:
                </div>
                <Link to={"/post"}>New Post</Link>
            </>}
            {/* Other authors */}
            {props.type === PostStreamTy.Author && props.authorID !== null && extractAuthorIdFromApi(props.authorID) !== getUserId() && <>
                <div>
                    This author has no posts.
                </div>
            </>}

            {/* Single post */}
            {props.type === PostStreamTy.Single && <>
                <div>
                    This post doesn't exist or is private.
                </div>
            </>}
        </div>
    )
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
        let response: PostsResponse|PostsStreamResponse;
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
                    if (postResponse.type === "post") {
                        const likes = await apiGetPostLikes(postResponse.author.id, postResponse.id);
                        const isLikedByUs = !!likes.items.find(like => extractAuthorIdFromApi(like.author.id) === getUserId());
                        return (
                            <Post
                                key={`${postResponse.author.id}/${postResponse.id}`}
                                {...postResponse} 
                                //@ts-ignore
                                likes={(likes.items).length}
                                isLiked={isLikedByUs}
                                refreshStream={() => {
                                    currentPage.current = 1;
                                    generatePosts(true);
                                }}
                            />
                        );
                    } else {
                        return <Ad key={postResponse.id} { ...postResponse } />;
                    }
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
            {posts.length > 0 ? 
                (posts.map((post, index) => (
                <div className={styles.postStreamPostContainer} key={post.key} ref={index === posts.length - 1 ? postRef : null}>
                    {post}
                </div>))
                ) : (
                <div className={styles.postStreamPostContainer}>
                    <EmptyStreamMessage type={props.type} authorID={props.authorID} />
                </div>
            )}
        </div>
    )
}

export default PostStream
