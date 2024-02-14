import { baseURL } from "../constants"
import { apiRequest } from "../utils/request";

import { 
    PaginatedAPI,
    AuthorsResponse,
    Author  
} from "./types";

/**
 * @description function to access the /authors view API.
 */
export const getAuthors = async (page: number, size: number) 
    : Promise<PaginatedAPI<AuthorsResponse>> => 
{    
    const response = await apiRequest(`${baseURL}/api/authors/?page=${page}&size=${size}`);
    const data: PaginatedAPI<AuthorsResponse> = await response.json();

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