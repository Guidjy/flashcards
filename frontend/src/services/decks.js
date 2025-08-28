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