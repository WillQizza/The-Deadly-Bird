import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";

/**
 * @description function to retreive the Stripe checkout URL
 */
export const apiGetSubscriptionURL = async (
  type: "annual" | "monthly"
): Promise<string> => {
    const response = await apiRequest(`${baseURL}/api/subscription/checkout?type=${type}`);    
    const data = await response.json(); 
    return data.url;
};

/**
 * @description function to check if user is currently subscribed
 */
export const apiCheckSubscriptionStatus = async (): Promise<boolean> => {
  const response = await apiRequest(`${baseURL}/api/subscription/check`);
  const data = await response.json();
  return data.status;
};