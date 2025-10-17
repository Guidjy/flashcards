import api from "./makeRequestWithAuth";


export async function cardsGetByDeckId(deckId) {
    try {
        const response = await api.get(`cards/?deck=${deckId}`);
        return response.data;
    } catch (error) {
        console.log('request failed: ', error);
        return false;
    }
}


export async function cardCreate(formData) {
    try {
        const response = await api.post('cards/', formData);
        return response.data;
    } catch (error) {
        console.log('request failed: ', error);
        return false;
    }
}