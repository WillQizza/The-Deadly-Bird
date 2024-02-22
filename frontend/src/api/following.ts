import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
import { FollowersResponse } from "./types";

/**
 * @description function to retreive the followers for an author
 * @param id author id to retrieve
 */
export const apiGetFollowers = async (
    authorID: string,
    page: number,
    size: number
): Promise<FollowersResponse> => {
    
    const response = await apiRequest(
        `${baseURL}/api/authors/${authorID}/followers?page=${page}&size=${size}`

    );    
    const data: FollowersResponse = await response.json(); 
    return data;
}

/**
 * @description function to retreive paginated list of authors authorID is following
 * @param id author id to retrieve
 * @param includeAuthorIDS a filter list of author ids to include in query
 * @param excludeAuthorIDS a filter list of author ids to exclude from query
 */
export const apiGetFollowing = async (
    authorID: string,
    page: number,
    size: number,
    includeAuthorIDs?: string[],
    excludeAuthorIDs?: string[]
): Promise<FollowersResponse> => {
    
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

export const apiFollowRequest = async( localAuthorId: string, foreignAuthorId: string)
: Promise<any> => {
    
    console.log("SEND FOLLOW REQUEST: local: ", localAuthorId, "foreign:", foreignAuthorId);

    const init: RequestInit = {
        method: "POST",
    }

    const response = await apiRequest(
        `${baseURL}/api/authors/request-follower/${localAuthorId}/${foreignAuthorId}`,
        init
    );
    
    const data = await response.json();
    console.log("RESPONSE DATA:", data);
    return data;
}

/**
 * @description remove foreign author as a follower of author id.   
 * @param authorId author that following
 * @param foreignAuthorId author that is being followed
 */
export const apiDeleteFollower = async (authorId: string, foreignAuthorId: string )
: Promise<number> => {
    const response = await fetch(`${baseURL}/api/authors/${authorId}/followers/${foreignAuthorId}`, {
        method: "DELETE",
    });
    
    return response.status;
}

/**
 * @description idempontent PUT to add foreign author as a follower of author id.   
 * @param authorId author that following
 * @param foreignAuthorId author that is being followed
 */
export const apiPutFollower = async (authorId: string, foreignAuthorId: string)
: Promise<number> => {
    const response = await fetch(`${baseURL}/api/authors/${authorId}/followers/${foreignAuthorId}`, {
        method: "PUT",
    });
    return response.status;
}

export const apiGetFollower = async (authorId: string, foreignAuthorId: string)
: Promise<any> => {
    const response = await fetch(`${baseURL}/api/authors/${authorId}/followers/${foreignAuthorId}`, {
        method: "GET",
    });
    if (!response.ok) {
        return {"status": response.status};
    }
    const data = await response.json();
    return data; 
}