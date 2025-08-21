import axios from "axios";
import createAuthRefreshInterceptor from "axios-auth-refresh";


// axios instance
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE,
});

// function that is called to refresh the access token
// 0-0: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
async function refreshAuth(failedRequest) {
    try {
        const refreshToken = localStorage.getItem("refreshToken");

        // refreshes the access token
        const response = await api.post("accounts/api/token/refresh/", {
            refresh: refreshToken,
        });
        const newAccessToken = response.data.access;
        localStorage.setItem("accessToken", newAccessToken);
        
        // updates failed request with new access token
        failedRequest.response.config.headers["Authorization"] = `Bearer ${newAccessToken}`;
        console.log("token refreshed");

        // retrues original failed request
        return Promise.resolve();
    } catch (error) {
        console.error("Failed to refresh access token: ", error);
        // redirects user to login page
        window.location.href = "/login";

        // doesn't retry original request
        return Promise.reject(error);
    }
}

// adds refresh logic to axios
createAuthRefreshInterceptor(api, refreshAuth);

// adds access token to all requests
api.interceptors.request.use((request) => {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
        request.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return request;
});

// exports axios instance so that every api call can have this behaviour
export default api;