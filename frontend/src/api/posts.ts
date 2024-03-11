import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
import { PostResponse, PostsResponse } from "./types";

/**
 * @description function to retreive the posts from an author
 * @param authorID to retreive posts from
 */
export const apiGetAuthorPosts = async (
    authorID: string,
    page: number,
    size: number
): Promise<PostsResponse> => {
    const response = await apiRequest(
        `${baseURL}/api/authors/${authorID}/posts/?page=${page}&size=${size}`
    );    
    const data: PostsResponse = await response.json(); 
    return data;
}

export enum APIPostStreamTy {
    Public = 'public',
    Following = 'following',
}
/**
 * @description function to retreive the public posts
 * @param type is the type of post stream to get
 */
export const apiGetPosts = async (
    type: APIPostStreamTy,
    page: number,
    size: number,
): Promise<PostsResponse> => {
    const response = await apiRequest(
        `${baseURL}/api/posts/${type}?page=${page}&size=${size}`
    );    
    const data: PostsResponse = await response.json(); 
    return data;
}

export const apiGetPost = async (
    authorID: string,
    postID: string,
): Promise<PostResponse | null> => {
    const response = await apiRequest(
        `${baseURL}/api/authors/${authorID}/posts/${postID}`
    );
    if (!response.ok) {
        return null;
    } else {
        const data: PostResponse = await response.json();
        return data;
    }
}

/**
 * @description delete a post locally or from remote
 * @param authorId author whose post is to be removed
 * @param postId post of author to remove
 */
export const apiDeletePosts = async (authorId: string, postId: string): Promise<any> => {
    console.log(authorId, postId); 
    const init: RequestInit = {
        "method": "delete"
    }
    const response = await apiRequest(
        `${baseURL}/api/authors/${authorId}/posts/${postId}`, init
    );

    // const data: any = await response.json();
    return response;
}
