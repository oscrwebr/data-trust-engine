import axios from "axios";
import { setAccessToken, getAccessToken } from "../Auth/authStore.js";

const test = import.meta.env.VITE_BACKEND_HOST || "localhost"
const api = axios.create({
  baseURL: `http://${test}:8000`,
  withCredentials: true
});

api.interceptors.request.use(function (config) {
  
  config.url != "/auth/sign-in" ? config.headers.Authorization = `Bearer ${getAccessToken()}` : null;
  return config
}, function (error) {
  return Promise.reject(error)
});

api.interceptors.response.use(
  function (response) {
    return response;
  }, async function (error) {
    const original_request = error.config;

    // Check if the original request has been retried yet and if the status is the expected unauthorised
    if (
      error.response.status === 401 
      && !original_request._retry 
      && original_request.url !== "/auth/token/refresh"
      ) {
      original_request._retry = true;
      try {
        const response = await api.get("/auth/token/refresh");
        setAccessToken(response.data.access_token);
        return api(original_request);

      } catch (error) {
        // This is incase the user actually needs to reauthenticate because the backend hasn't accepted the refresh, etc
        window.location.href = "http://localhost:8000/auth/sign-in?next=" + window.location.pathname;
      }
      
    }
    
    return Promise.reject(error);
  });

export default api;
