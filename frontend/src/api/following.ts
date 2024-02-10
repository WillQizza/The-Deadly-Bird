import { baseURL } from "../constants";
import { Author } from "./authors";

export type FollowersAPIResponse = {
    type: string;
    items: Author[];
};

export type APIResponse = {
    count: number,
    next: number | null,
    previous: number | null,
    results: FollowersAPIResponse
};

export const getFollowers = async (
    authorID: number,
    page: number,
    size: number
): Promise<APIResponse> => {
    
    const response = await fetch(
        `${baseURL}/api/authors/${authorID}/followers?page=${page}&size=${size}`
    );
    
    const data: APIResponse = await response.json();
    return data;
}
