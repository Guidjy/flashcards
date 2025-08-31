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