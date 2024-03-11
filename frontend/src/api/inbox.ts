import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
import { InboxResponse } from "./types";
import { apiGetAuthor } from "./authors";
/**
 * @description function to retreive inbox mesages for an author
 * @param id author id to retrieve
 */
export const getInboxMessages = async (
    authorID: string,
    page: number,
    size: number
): Promise<InboxResponse> => {
    
    const inboxAuthor = (await apiGetAuthor(authorID))!;
    const response = await fetch(
        `${inboxAuthor.host}/authors/${authorID}/inbox?page=${page}&size=${size}`
    );   
    console.log("response:", response);
    const data: InboxResponse = await response.json(); 
    console.log("response json:", data);
    return data;
}

/**
 * @description function to retreive inbox mesages for an author
 * @param id author id whose inbox to clear
 */
export const apiClearInbox = async (authorID: string): Promise<any> => {
    const inboxAuthor = (await apiGetAuthor(authorID))!;
    const init: RequestInit = {
        method: "DELETE"
    }; 
    const response = await apiRequest(
        `${inboxAuthor.host}/authors/${authorID}/inbox`, init
    );   
    return response; 
}