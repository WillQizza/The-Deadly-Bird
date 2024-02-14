import { baseURL } from "../constants";
import { Author, PaginatedAPI, InboxResponse } from "./types";

/**
 * @description function to retreive inbox mesages for an author
 * @param id author id to retrieve
 */
export const getInboxMessages = async (
    authorID: number,
    page: number,
    size: number
): Promise<PaginatedAPI<InboxResponse>> => {
    
    const response = await fetch(
        `${baseURL}/api/authors/${authorID}/inbox?page=${page}&size=${size}`
    );    
    const data: PaginatedAPI<InboxResponse> = await response.json();
    
    return data;
}