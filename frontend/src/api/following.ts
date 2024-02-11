import { baseURL } from "../constants";
import { Author, PaginatedAPI, FollowersResponse } from "./types";

/**
 * @description function to retreive the followers for an author
 * @param id author id to retrieve
 */
export const getFollowers = async (
    authorID: number,
    page: number,
    size: number
): Promise<PaginatedAPI<FollowersResponse>> => {
    
    const response = await fetch(
        `${baseURL}/api/authors/${authorID}/followers?page=${page}&size=${size}`
    );    
    const data: PaginatedAPI<FollowersResponse> = await response.json();
    
    return data;
}