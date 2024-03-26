import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
import { extractAuthorIdFromApi, extractPostIdFromApi } from "./utils";

export const apiGetComments = async (
  authorId: string,
  postId: string,
  page: number = 1,
  size: number = 10,
) => {
  const response = await apiRequest(`${baseURL}/api/authors/${extractAuthorIdFromApi(authorId)}/posts/${extractPostIdFromApi(postId)}/comments?page=${page}&size=${size}`);

  const data = await response.json();
  return data;
};

export const apiPostComment = async (
  authorId: string,
  postId: string,
  {
    comment,
    contentType
  } : { comment: string, contentType: string }
) => {
  const formData = new URLSearchParams({
      comment,
      contentType
  }).toString();

  const response = await apiRequest(`${baseURL}/api/authors/${extractAuthorIdFromApi(authorId)}/posts/${extractPostIdFromApi(postId)}/comments`, {
      method: "POST",
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData
  });

  if (!response.ok) {
    return null;
  } else {
    const json = await response.json();
    return json;
  }
};