import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
import { Post, PostResponse, PostsResponse } from "./types";
import { extractAuthorIdFromApi, extractPostIdFromApi } from "./utils";

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
        `${baseURL}/api/authors/${extractAuthorIdFromApi(authorID)}/posts/?page=${page}&size=${size}`
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
        `${baseURL}/api/authors/${extractAuthorIdFromApi(authorID)}/posts/${extractPostIdFromApi(postID)}`
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
        `${baseURL}/api/authors/${extractAuthorIdFromApi(authorId)}/posts/${extractPostIdFromApi(postId)}`, init
    );

    // const data: any = await response.json();
    return response;
}

/**
 * @description share a post
 * @param authorId author whose post is to be shared
 * @param postId post of author to share
 */
export const apiSharePost = async (authorId: string, postId: string): Promise<Post|null> => {
    const response = await apiRequest(`${baseURL}/api/authors/${extractAuthorIdFromApi(authorId)}/posts/${extractPostIdFromApi(postId)}/share`, {
        method: "POST"
    });

    const json = await response.json();

    if (response.status === 201) {
        return json as Post;
    } else {
        return null;
    }
}