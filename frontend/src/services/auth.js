const API_BASE = 'http://localhost:8000';

export function login(username, password) {
    fetch(`${API_BASE}/api/token/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json)
    .then(data => {
        if (data.access) {
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);
            log({ message: 'Login successful', tokens: data });
        } else {
            log({ error: 'Login failed', details: data });
        }
   })
    .catch(err => log({ error: 'Request failed', details: err }));
}


export function logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    log({ message: 'Logged out' });
}