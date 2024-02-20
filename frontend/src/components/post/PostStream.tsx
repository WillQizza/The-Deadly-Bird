import React, { useEffect, useState } from 'react';
import styles from './PostStream.module.css';
import Post from './Post';
import { Post as PostTy } from '../../api/types';
import { apiGetAuthorPosts } from '../../api/posts';
import { getUserId } from '../../utils/auth';

const PostStream: React.FC = () => {
    const [posts, setPosts] = useState<React.ReactElement[]>([])

    useEffect(() => {
        // function to add posts to current posts
        const addPosts = (newPosts: React.ReactElement[]) => {
            setPosts([...posts, ...newPosts]);
        };

        // generate all posts
        const curAuthorId = getUserId(); 
        apiGetAuthorPosts(curAuthorId, 1, 5)
            .then(async response => {
                const newPosts = response.items.map((postResponse) => {
                    // remove comments and commentsSrc fields from post response
                    // TODO: this will probably be needed when comments are implemented
                    const { comments, commentsSrc, ...post} = postResponse;
                    return <Post key={post.id} {...post} />;
                })
                addPosts(newPosts);
            });
    }, []);

    return (
        <div className={styles.postStream}>
            {posts.map(post => post)}
        </div>
    )
}

export default PostStream
