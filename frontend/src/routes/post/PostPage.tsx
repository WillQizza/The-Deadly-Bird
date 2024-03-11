import React from "react";
import Page from "../../components/layout/Page";
import { useParams } from 'react-router-dom';
import PostStream, { PostStreamTy } from "../../components/post/PostStream";

const PostPage: React.FC = () => {
    const params = useParams();
    const authorID = params["author"];
    const postID = params["post"];

    return <Page>
        <PostStream type={PostStreamTy.Single} authorID={authorID ? authorID : null} postID={postID ? postID : null} />
    </Page>;
}

export default PostPage;
