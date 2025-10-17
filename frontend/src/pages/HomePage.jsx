import MainLayout from "../layouts/MainLayout"
// components
import Table from "../components/Table"
import { Link } from "react-router-dom";
import CreateDeckButton from "../components/CreateDeckButton";
import EditDeckButton from "../components/EditDeckButton";
// services
import { getUserDecks } from "../services/decks";
// hooks
import { useState, useEffect } from "react"


export default function HomePage() {

  const [decks, setDecks] = useState([]);
  const [deckCreated, setDeckCreated] = useState(false);

  useEffect(() => {
    async function fetchDecks() {
      // gets currently logged in user's decks
      const response = await getUserDecks();
      console.log(response);

      // adds them to a list
      let deckList = [];
      if (response) {
        response.map((deck, index) => {
          deckList.push(
            <tr key={deck.id}>
              <td>{index + 1}</td>
              <td>
                <Link className="link link-secondary" to={`/deck/${deck.id}`}>
                  {deck.name}
                </Link>
              </td>
              <td>{deck.card_count}</td>
              <td>
                <EditDeckButton deckId={deck.id} deckName={deck.name} onDeckCreate={() => setDeckCreated(true)}/>
              </td>
            </tr>
          );
        });

        setDecks(deckList);
      }
    }

    setDeckCreated(false);
    fetchDecks();
  }, [deckCreated]);

  return (
    <>
      <MainLayout>
        <Table
          columns={["Name", "Cards", "Edit"]}
          rows={decks}
        />
      <CreateDeckButton onDeckCreate={() => setDeckCreated(true)} />
      </MainLayout>
    </>
  );
}