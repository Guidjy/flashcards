import api from "./makeRequestWithAuth";


export async function getUserDecks() {
    try {
        const response = await api.get('get-user-decks');
        return response.data
    } catch (error) {
        console.log('request failed: ', error);
        return false;
    }
}


export async function deckCreate(deckName) {
    try {
        const response = await api.post('decks/', {
            name: deckName,
            owned_by: localStorage.getItem("userId")
        });
        return response.data;
    } catch (error) {
        console.log("request failed: ", error);
        return false;
    }
}


export async function deckGet(deckId) {
    try {
        const response = await api.get(`decks/${deckId}`);
        return response.data;
    } catch (error) {
        console.log("request failed: ", error);
        return false;
    }
}