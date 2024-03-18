import { baseURL } from "../constants";
import { apiRequest } from "../utils/request";
/**
 * @description function to retreive the hostname of app.
 */
export const apiGetHostname = async (
): Promise<any> => {
    const response = await apiRequest(`${baseURL}/api/hostname/`);    
    const data: any = await response.json(); 
    return data;
}