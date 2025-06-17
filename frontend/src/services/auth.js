const API_BASE = 'http://localhost:8000';


export async function register(username, email, password, passwordConfirmation) {
    fetch(`${API_BASE}/registrar/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nome: username,
            email: email,
            senha: password,
            confirmacaoSenha: passwordConfirmation,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Registration response:', data);
    })
}


export async function login(username, password) {
    fetch(`${API_BASE}/api/token/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);
            console.log({ message: 'Login successful', tokens: data });
            return true;
        } else {
            console.log({ error: 'Login failed', details: data });
            return false;
        }
   })
}


export function logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    log({ message: 'Logged out' });
}