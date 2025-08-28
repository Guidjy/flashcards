import MainLayout from "../layouts/MainLayout"
// components
import Table from "../components/Table"
import { Link } from "react-router-dom";
// services
import { getUserDecks } from "../services/decks";
// hooks
import { useState, useEffect } from "react"


export default function HomePage() {

  const [decks, setDecks] = useState([]);

  useEffect(() => {
    async function fetchDecks() {
      // gets currently logged in user's decks
      const response = await getUserDecks();

      // adds them to a list
      let deckList = [];
      if (response) {
        response.decks.map((deck) => {
          deckList.push(
            <tr key={deck.id}></tr>
          );
        });

        console.log(deckList);
        setDecks(deckList);
      }
    }
    fetchDecks();
  }, []);

  return (
    <>
      <MainLayout>
        <Table
          columns={["Name", "Cards", "Edit"]}
          rows={decks.map((deck) => {
            return {"name": deck.name, "cards": deck.cardCount};
          })}
        />
      </MainLayout>
    </>
  )
}