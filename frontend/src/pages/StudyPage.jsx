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
  const [cardsReviewd, setCardsReviewd] = useState(0);
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [deck, setDeck] = useState({});
  
  const { deckId } = useParams();

  useEffect(() => {
    // fetches the deck and card order
    async function fetchDeck(id) {
      const response = await deckGet(id);
      setDeck(response);
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
      <div className="flex justify-center w-full h-screen">
        <div className="flex flex-col items-center w-full md:w-4/5 lg:w-2/3 xl:w-1/2 p-10 md:p-15">
          <FlashCard
            front={cards[0].front}
            back={cards[0].back}
            image={cards[0].image}
          />
        </div>
      </div>
    </>
  )
}