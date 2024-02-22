import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
import { PostsResponse } from "./types";

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

/**
 * @description function to retreive the public posts
 */
export const apiGetPublicPosts = async (
    page: number,
    size: number
): Promise<PostsResponse> => {
    const response = await apiRequest(
        `${baseURL}/api/posts/public?page=${page}&size=${size}`
    );    
    const data: PostsResponse = await response.json(); 
    return data;
}
