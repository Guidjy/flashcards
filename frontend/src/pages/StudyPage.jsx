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
  }, [deckId])

  return (
    <>
      <span className="badge absolute">{correctAnswers}/{cardCount}</span>
      <div className="flex justify-center items-center w-full h-screen bg-base-300">
        <FlashCard
          front={cards[0].front}
          back={cards[0].back}
          image={cards[0].image}
        />
      </div>
    </>
  )
}