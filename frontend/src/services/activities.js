import api from "./makeRequestWithAuth";

// WARNING: there's a typo in my database -"cards_reviewed" is actually "cards_reviewd" (without an "e" before the final "d")-.
// my lazy ass is NOT gonna run migrations back in django so just keep that in mind as you read ts.


export async function createOrUpdateActivity(cardsReviewed, correctAnswers, deckId) {
    // checks if a there is already activity for today for this deck
    const userId = localStorage.getItem("userId");
    const today = new Date().toISOString().split("T")[0];  // YYYY-MM-DD format
    const activityToday = await api.get(`activities/?user=${userId}&date=${today}&deck=${deckId}`);
    console.log(activityToday.data);

    if (activityToday.data.length === 0) {
        // creates an activity object for today for this deck
        const response = await api.post("activities/", {
            cards_reviewd: cardsReviewed,
            correct_answers: correctAnswers,
            deck: deckId,
            user: userId
        });
        console.log(response.data);
        
        return response.data;
    }

    const response = await api.patch(`activities/${activityToday.data[0].id}/`, {
        cards_reviewd: cardsReviewed,
        correct_answers: correctAnswers,
    });
    console.log(response.data);
    return response.data;

}