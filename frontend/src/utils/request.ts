const DJANGO_COOKIE_NAME = "csrftoken";

/**
 * Extracts Django's CSRFToken that all requests need
 */
const extractCSRFToken = () => {
  const csrfCookieStr = document.cookie.split("; ")
    .find(cookie => cookie.startsWith(DJANGO_COOKIE_NAME));

  if (!csrfCookieStr) {
    return null;
  }

  return csrfCookieStr.split("=").slice(1).join("=");
};

/**
 * Proxy for fetch except with it always sends the X-CSRFToken header if available
 * @param input
 * @param init 
 * @returns regular fetch response
 */
export const apiRequest = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
  const data = Object.assign({
    credentials: "include"
  }, init || {});

  const headers = new Headers(data.headers);
  const csrfToken = extractCSRFToken();

  if (csrfToken !== null) {
    headers.set("X-CSRFToken", csrfToken);
  }

  data.headers = headers;
  return fetch(input, data);
};
