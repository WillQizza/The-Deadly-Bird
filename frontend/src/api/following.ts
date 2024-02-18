import { baseURL } from "../constants";
import { Author, PaginatedAPI, FollowersResponse } from "./types";
import { apiRequest } from "../utils/request";

/**
 * @description function to retreive the followers for an author
 * @param id author id to retrieve
 */
export const apiGetFollowers = async (
    authorID: number,
    page: number,
    size: number
): Promise<PaginatedAPI<FollowersResponse>> => {
    
    const response = await apiRequest(
        `${baseURL}/api/authors/${authorID}/followers?page=${page}&size=${size}`
    ); 
    const data = await response.json();
    
    return data;
}

/**
 * @description function to retreive paginated list of authors authorID is following
 * @param id author id to retrieve
 * @param includeAuthorIDS a list of author ids to exclusively include in query
 * @param excludeAuthorIDS a list of author ids to exclude from query
 */
export const apiGetFollowing = async (
    authorID: string,
    page: number,
    size: number,
    includeAuthorIDs?: string[],
    excludeAuthorIDs?: string[]
): Promise<PaginatedAPI<FollowersResponse>> => {
    
    const url = new URL(`${baseURL}/api/authors/${authorID}/followers`);
    const params = new URLSearchParams(url.search);

    params.set('page', page.toString());
    params.set('size', size.toString());

    if (includeAuthorIDs?.length) {
        params.set('include_author_ids', includeAuthorIDs.join(','));
    }
    if (excludeAuthorIDs?.length) {
        params.set('exclude_author_ids', excludeAuthorIDs.join(','));
    }
    url.search = params.toString();

    const response = await fetch(url.toString());
    const data = await response.json();

    return data; 
}


export const apiFollowRequest = async(
    localAuthorId: string,
    foreignAuthorId: string
): Promise<any> => {
    
    const init: RequestInit = {
        method: "POST",
    }

    const response = await apiRequest(
        `${baseURL}/api/authors/request-follower/${localAuthorId}/${foreignAuthorId}`,
        init
    );
    const data = await response.json();

    return data;
}

export const apiDeleteFollower = async (
    authorId: string,
    foreignAuthorId: string
): Promise<any> => {
    const response = await fetch(`${baseURL}/api/authors/${authorId}/followers/${foreignAuthorId}`, {
        method: "DELETE",
    });
    const data = await response.json();
    return data;
}

export const apiPutFollower = async (
    authorId: string, 
    foreignAuthorId: string
): Promise<any> => {
    const response = await fetch(`${baseURL}/api/authors/${authorId}/followers/${foreignAuthorId}`, {
        method: "PUT",
    });
    const data = await response.json();
    return data;
}

export const apiGetFollower = async (
    authorId: string, 
    foreignAuthorId: string
): Promise<any> => {
    const response = await fetch(`${baseURL}/api/authors/${authorId}/followers/${foreignAuthorId}`, {
        method: "GET",
    });
    const data = await response.json();
    return data;
}
