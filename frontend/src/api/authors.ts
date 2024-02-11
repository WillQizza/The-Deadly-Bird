import { baseURL } from "../constants"
import { apiRequest } from "../utils/request";

export type Author = {
    type: string;
    id: string;
    url: string;
    host: string;
    displayName: string;
    github?: string;
    profileImage?: string;
    posts: number;
    following: number;
    followers: number;
};

export type AuthorsAPIResponse = {
    type: string;
    items: Author[];
};

export type APIResponse = {
    count: number,
    next: number | null,
    previous : number | null,
    results: AuthorsAPIResponse 
};

/**
 * @description function to access the /authors view API.
 * 
 */
export const getAuthors = async (page: number, size: number) : Promise<APIResponse> => {
    const response = await apiRequest(`${baseURL}/api/authors/?page=${page}&size=${size}`);

    const data: APIResponse = await response.json();
    return data;
}

/**
 * @description function to access the /authors/id view API.
 * @param id author id to retrieve

 */
export const getAuthor = async (id: number): Promise<Author|null> => {
    const response = await apiRequest(`${baseURL}/api/authors/${id}/`);

    if (response.status === 404) {
        return null;
    }
    
    const data: Author = await response.json();
    return data;
};