// hooks
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
// services
import { deckGet } from "../services/decks";
import { cardsGetByDeckId } from "../services/cards";


export default function StudyPage() {

  const [cards, setCards] = useState([]);
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
      {cards.map((card) => {return (
        <h1>{card.front}</h1>
      )})}
    </>
  )
}