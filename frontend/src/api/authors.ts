import { baseURL } from "../constants"

export type Author = {
    type: string;
    id: string;
    url: string;
    host: string;
    displayName: string;
    github: string;
    profileImage: string;
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
    
    const response = await fetch(baseURL+`/api/authors/?page=${page}&size=${size}`);
    const data: APIResponse = await response.json();

    return data;
}