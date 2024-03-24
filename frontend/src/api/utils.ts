export const extractAuthorIdFromApi = (apiId: string) => {
  if (apiId.includes("http")) {
    // API link
    return apiId.split("/").slice(-1)[0];
  } else {
    // Raw id
    return apiId;
  }
};