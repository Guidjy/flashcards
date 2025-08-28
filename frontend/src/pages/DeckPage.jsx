// layout
import MainLayout from "../layouts/MainLayout";
// hooks
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
// services
import { deckGet } from "../services/decks";


export default function DeckPage() {
  

  const [deck, setDeck] = useState(null);
  
  const { deckId } = useParams();

  useEffect(() => {
    async function fetchDeck(id) {
      const response = await deckGet(id);
      setDeck(response);
    }
    fetchDeck(deckId);
  }, [deckId])


  return (
    <>
      <MainLayout>
        {deckId}
      </MainLayout>
    </>
  );
}