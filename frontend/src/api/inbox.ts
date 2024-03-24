import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
import { InboxResponse } from "./types";
import { extractAuthorIdFromApi } from "./utils";
/**
 * @description function to retreive inbox mesages for an author
 * @param id author id to retrieve
 */
export const getInboxMessages = async (
    authorID: string,
    page: number,
    size: number
): Promise<InboxResponse> => {
    const response = await apiRequest(
        `${baseURL}/api/authors/${extractAuthorIdFromApi(authorID)}/inbox?page=${page}&size=${size}`,
        {method: "GET"}
    );   
    const data: InboxResponse = await response.json(); 
    return data;
}

/**
 * @description function to retreive inbox mesages for an author
 * @param id author id whose inbox to clear
 */
export const apiClearInbox = async (authorID: string): Promise<any> => {
    const init: RequestInit = {
        method: "DELETE"
    }; 
    const response = await apiRequest(
        `${baseURL}/api/authors/${extractAuthorIdFromApi(authorID)}/inbox`, init
    );   
    return response; 
}