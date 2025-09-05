// hooks
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
// components
import FlashCard from "../components/FlashCard";
// services
import { deckGet } from "../services/decks";
import { cardsGetByDeckId } from "../services/cards";


export default function StudyPage() {

  const [cards, setCards] = useState([{}]);
  const [cardCount, setCardCount] = useState(0);
  const [cardsReviewd, setCardsReviewd] = useState(0);
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [deck, setDeck] = useState({});
  const [studyFinished, setStudyFinished] = useState(false);
  
  const { deckId } = useParams();


  useEffect(() => {
    // fetches the deck and card order
    async function fetchDeck(id) {
      const response = await deckGet(id);
      setDeck(response);
      setCardCount(response.card_count);
    }
    fetchDeck(deckId);
    
    // fetches the cards
    async function fetchCards(deckId) {
      const response = await cardsGetByDeckId(deckId);
      setCards(response);
    }
    fetchCards(deckId);
  }, [deckId]);


    function onAnswer(correct) {
    let cards_copy = cards;
    if (correct) {
      // checks if all cards have been correctly answered
      // this check hast to be done here or else react would try to render a card when the list is empty, causing an error
      if (correctAnswers === cardCount-1) {
        setStudyFinished(true);
        setCorrectAnswers(correctAnswers+1);
        setCardsReviewd(cardsReviewd+1);
        return;
      }
      // removes the card from the review list
      cards_copy.shift();
      setCards(cards_copy);
      setCorrectAnswers(correctAnswers+1);
      setCardsReviewd(cardsReviewd+1);
    } else {
      // moves the card to the middle of the deck
      const middle = Math.round(cards.length / 2);
      // weird ahh method: inserts cards[0] into cards[middle] and deletes 0 elements
      cards_copy.splice(middle, 0, cards[0]);
      cards_copy.shift();
      setCards(cards_copy);
      setCardsReviewd(cardsReviewd+1);
    }
  }


  return (
    <>
      <span className="badge absolute">{correctAnswers}/{cardCount}</span>
      <div className="flex justify-center items-center w-full h-screen bg-base-300">
        {studyFinished ? (
          <h1>finished!!!1!!</h1>
        ) : (
          <FlashCard
            front={cards[0].front}
            back={cards[0].back}
            image={cards[0].image}
            onAnswer={onAnswer}
          />
        )}
      </div>
    </>
  )
}