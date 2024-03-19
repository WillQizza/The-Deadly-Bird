import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
import { FollowersResponse } from "./types";
import { Author } from "./types";
import { apiGetAuthor } from "./authors";

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

    const response = await apiRequest(url.toString());
    const data = await response.json();

    return data; 
}

/**
 * @description POST inbox message of type "Follow" to node in fromAuthors host field.
 * @param fromAuthorID Author on local who pushes "Follow" button 
 * @param toAuthorID Receiving Author, may be local or remote
 */   
export const apiInboxFollowRequest = async (
    fromAuthorID: string,
    toAuthorID: string,
) 
: Promise<any> => { 
    try {
        const fromAuthor = (await apiGetAuthor(fromAuthorID))!;
        const toAuthor = (await apiGetAuthor(toAuthorID))!;
        
        const response = await apiRequest(`${baseURL}/api/authors/${toAuthor.id}/inbox/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "type": "Follow",
                "summary": `${fromAuthor.displayName} wants to follow ${toAuthor.displayName}`,
                "actor": fromAuthor,
                "object": toAuthor
            })
        });    
        const data: any = await response.json(); 
        return data;
    } catch(e) {
        return null;
    }    
}

export const apiGetFollowRequest = async(
    authorId: string, 
    targetAuthorId: string,
)
: Promise<any> => { 
    const init: RequestInit = {method: "GET",}
    const response = await apiRequest(
        `${baseURL}/api/authors/request-follower/${authorId}/${targetAuthorId}`,
        init
    );
    const data = await response.json();
    return data;
}

/**
 * @description remove foreign author as a follower of author id.   
 * @param authorId author that following
 * @param foreignAuthorId author that is being followed
 */
export const apiDeleteFollower = async (authorId: string, foreignAuthorId: string )
: Promise<number> => {
    const response = await apiRequest(`${baseURL}/api/authors/${authorId}/followers/${foreignAuthorId}`, {
        method: "DELETE",
    });
    
    return response.status;
}

/**
 * @description PUT to add author as a follower of target author.   
 * @param authorId author that following
 * @param foreignAuthorId author that is being followed
 */
export const apiPutFollower = async (authorId: string, targetAuthorId: string)
: Promise<number> => {

    const response = await apiRequest(`${baseURL}/api/authors/${targetAuthorId}/followers/${authorId}`, {
        method: "PUT",
    });
    return response.status;
}

export const apiGetFollower = async (authorId: string, foreignAuthorId: string)
: Promise<any> => {
    const response = await apiRequest(`${baseURL}/api/authors/${authorId}/followers/${foreignAuthorId}`, {
        method: "GET",
    });
    if (!response.ok) {
        return {"status": response.status};
    }
    const data = await response.json();
    return data; 
}