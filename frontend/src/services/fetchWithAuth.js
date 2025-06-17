import { login, logout } from "./auth";

const API_BASE = 'http://localhost:8000';

export async function fetchWithAuth(url, options = {}) {
    // gets access and refresh tokens
    const access = localStorage.getItem('access');
    const refresh = localStorage.getItem('refresh');

    // checks if the tokens exist
    if (!access || !refresh) {
        log({ error: 'Not logged in' });
        throw new Error('Not logged in');
    }

    // request headers
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
        'Authorization': `Bearer ${access}`,
    };

    // makes request
    let response = await fetch(url, { ...options, headers });

    // if there is an authentication error
    if (response.status === 401) {
        // Try refreshing the access token
        const refreshResponse = await fetch(`${API_BASE}/api/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh }),
        });

        if (refreshResponse.ok) {
            const data = await refreshResponse.json();
            localStorage.setItem('access', data.access);

            // Retry original request with new access token
            headers['Authorization'] = `Bearer ${data.access}`;
            response = await fetch(url, { ...options, headers });
        } else {
            // Refresh failed, force logout (refresh token is probably expired)
            logout();
            log({ error: 'Session expired. Please log in again.' });
            throw new Error('Session expired');
        }
    }

    const jsonData = await response.json();
    return jsonData;
}