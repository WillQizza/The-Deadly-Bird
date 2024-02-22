const USER_ID_KEY = "user-id";

export const getUserId = () => localStorage.getItem(USER_ID_KEY)!;
export const setUserId = (id: string) => localStorage.setItem(USER_ID_KEY, id);