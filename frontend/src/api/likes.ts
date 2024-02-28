import { baseURL } from "../constants";
import { LikesResponse } from "./types";
import { apiRequest } from "../utils/request";

/**
 * @description function to retreive the posts from an author
 * @param authorID to retreive posts from
 */
export const apiGetPostLikes = async (
    authorID: string,
    postID: string,
): Promise<LikesResponse> => {
    const response = await apiRequest(`${baseURL}/api/authors/${authorID}/posts/${postID}/likes/`);    
    const data: LikesResponse = await response.json(); 
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
): Promise<LikesResponse> => {
    const response = await apiRequest(`${baseURL}/api/authors/${authorID}/posts/${postID}/comments/${commentID}/likes/`);    
    const data: LikesResponse = await response.json(); 
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
    const response = await apiRequest(`${baseURL}/api/authors/${authorID}/posts/${postId}/likes/`, {
        method: "POST"
    });    
    const data: any = await response.json(); 
    return data;
}