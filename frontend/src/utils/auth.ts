const USER_ID_KEY = "user-id";

export const getUserId = () => localStorage.getItem(USER_ID_KEY)!;
export const setUserId = (id: string|null) => {
  if (id === null) {
    localStorage.removeItem(USER_ID_KEY);
  } else {
    localStorage.setItem(USER_ID_KEY, id);
  }
};