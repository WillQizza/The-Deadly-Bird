import { baseURL } from "../constants";
import { InboxResponse } from "./types";

/**
 * @description function to retreive inbox mesages for an author
 * @param id author id to retrieve
 */
export const getInboxMessages = async (
    authorID: string,
    page: number,
    size: number
): Promise<InboxResponse> => {
    
    const response = await fetch(
        `${baseURL}/api/authors/${authorID}/inbox?page=${page}&size=${size}`
    );    
    const data: InboxResponse = await response.json();
    
    return data;
}