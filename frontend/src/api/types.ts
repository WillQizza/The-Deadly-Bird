/**
 * @file types.ts 
 * @description Types for responses since GET requests will often
 * return terse objects.
 */

/* Wraps GET responses that return a paginated list. */
export type PaginatedAPI<T, R> = {
    type: T;
    next: string | null,
    prev: string | null,
    items: R[]
};

/* Basic Object Types */
export type Author = {
    type: "author";
    id: string;
    url: string;
    host: string;
    displayName: string;
    bio: string;
    email?: string;
    github?: string;
    profileImage?: string;
    blocked?: boolean;
    subscribed: boolean;
    posts: number;
    following: number;
    followers: number;
};

export type Post = {
    type: "post",
    id: string,
    title: string,
    source: string,
    origin: string,
    description: string,
    contentType: ContentType,
    content: string,
    author: Author,
    originAuthor?: Author,
    originId?: string,
    published: string,
    visibility: string,

    // extra fields
    unlisted: boolean | null //appears in the Inbox get request
};

export type Comment = {
    type: "comment",
    author: Author,
    comment: string,
    contentType: ContentType,
    published: string,
    id: string
};

export type Like = {
    type: "Like", // capitalized cause in spec it is >:(
    "@context": string,
    summary: string,
    author: Author,
    object: string
};

// url: ://service/authors/
export type AuthorsResponse = PaginatedAPI<"authors", Author>;

// url: ://service/authors/{AUTHOR_ID}/followers
export type FollowersResponse = PaginatedAPI<"followers", Author>;

// url : ? Not Specified in Spec.
export type FollowResponse = {
    type: "follow",
    summary: string,
    actor: Author,
    object: Author
};

// url: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
export type PostResponse = Post & {
    // flatten the Post type and add two extra fields
    comments: string | null,
    commentsSrc: any    
};

// url: ://service/authors/{AUTHOR_ID}/posts/
export type PostsResponse = PaginatedAPI<"posts", PostResponse>;

// url: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
export type CommentsResponse = PaginatedAPI<"comments", Comment>;

//url: ://service/authors/{AUTHOR_ID}/liked 
export type LikedResponse = {
    type: "liked",
    items: Like[]
};

export type LikesResponse = {
    type: "likes",
    items: Like[]
};

//url ://service/authors/{AUTHOR_ID}/inbox 
export type InboxResponse = {
    type: "inbox",
    author: number,
    items: (Post | Comment | Like)[]
}; // TODO: Add follow request type

export enum ContentType {
    MARKDOWN = "text/markdown",
    PLAIN = "text/plain",
    APPLICATION_BASE64 = "application/base64",
    PNG_BASE64 = "image/png;base64",
    JPEG_BASE64 = "image/jpeg;base64",
}
