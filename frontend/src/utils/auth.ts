const USER_ID_KEY = "user-id";

export const getUserId = () => parseInt(localStorage.getItem(USER_ID_KEY) || "-1");
export const setUserId = (id: number) => localStorage.setItem(USER_ID_KEY, id.toString());