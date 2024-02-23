import { baseURL } from "../constants";
import { LikedResponse } from "./types";
import { apiRequest } from "../utils/request";

/**
 * @description function to retreive the posts from an author
 * @param authorID to retreive posts from
 */
export const apiGetPostLikes = async (
    authorID: string,
    postID: string,
    page: number,
    size: number
): Promise<LikedResponse> => {
    const response = await apiRequest(
        `${baseURL}/api/authors/
            ${authorID}/posts/
            ${postID}/likes
            ?page=${page}&size=${size}`
    );    
    const data: LikedResponse = await response.json(); 
    return data;
}

/**
 * @description get comment likes for a post
 * @param authorID of post with comment to retreive likes from
 * @param postID post authorID likes
 * @param commentID comment of the 
*/
export const apiGetCommentLikes = async (
    authorID: string,
    postID: string,
    commentID: string,
    page: number,
    size: number
): Promise<LikedResponse> => {
    const response = await apiRequest(
        `${baseURL}/api/authors/
            ${authorID}/posts/
            ${postID}/comments/
            ${commentID}likes
            ?page=${page}&size=${size}`
    );    
    const data: LikedResponse = await response.json(); 
    return data;
}

/**
 * @description create a like object
 * @param authorID author initiating the like
 * @param postID post authorID likes
 */
export const apiCreateLike = async (
    authorID: string,
    postId: string
): Promise<any> => {
    const response = await apiRequest( 
        `${baseURL}/api/authors/${authorID}/posts/${postId}/likes`
    );    
    const data: any = await response.json(); 
    return data;
}