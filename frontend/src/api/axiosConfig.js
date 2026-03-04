import axios from "axios";
import { setAccessToken, getAccessToken } from "../Auth/authStore.js";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true
});

api.interceptors.request.use(function (config) {
  // console.log("this is the url being used currently: " + config.baseURL + config.url);
  // console.log("This is the access token: " + getAccessToken());
  
  config.url != "/auth/sign-in" ? config.headers.Authorization = `Bearer ${getAccessToken()}` : null;
  return config
}, function (error) {
  // console.log("This is the error - resquest: " + error)
  return Promise.reject(error)
});

api.interceptors.response.use(
  function (response) {
    // console.log(response);
    return response;
  }, async function (error) {
    const original_request = error.config;
      // console.log("THIS IS THE ORIGINAL REQUEST URL: " + original_request.url);
      // console.log("This is the response status for the error: " + error.response.status);
      // console.log("This is the retry value for the new variable: " + original_request._retry)

    // Check if the original request has been retried yet and if the status is the expected unauthorised
    if (
      error.response.status === 401 
      && !original_request._retry 
      && original_request.url !== "/auth/token/refresh"
      ) {
      original_request._retry = true;
      try {
        const response = await api.get("/auth/token/refresh");
        // console.log(`This is the second axios call: ${response} and this is the data within it: ${response.data}`);
        setAccessToken(response.data.access_token);
        // console.log(`Value of the axios toekn, now that refresh went through: ${getAccessToken()}`);
        // original_request.Authorization = `Bearer ${getAccessToken()}`;
        return api(original_request);

      } catch (error) {
        // This is incase the user actually needs to reauthenticate because the backend hasn't accepted the refresh, etc
        // api.get("auth/sign-in");
        // console.log("Trying to do sign in now!")
        // console.log(`THis is the error_retyr for forced sign in: ${error._retry}`)
        // console.log("current route: " + window.location.pathname);
        window.location.href = "http://localhost:8000/auth/sign-in?next=" + window.location.pathname;
      }
      
    }
    
    return Promise.reject(error);
  });

export default api;
