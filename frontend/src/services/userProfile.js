import { fetchWithAuth } from "./fetchWithAuth";

const API_BASE = 'http://localhost:8000';

export async function userProfile() {
    const profile = await fetchWithAuth(`${API_BASE}/perfil/`);
    return profile;
}