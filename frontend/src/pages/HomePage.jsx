import MainLayout from "../layouts/MainLayout"
// components
import Table from "../components/Table"
import { Link } from "react-router-dom";
import CreateDeckButton from "../components/CreateDeckButton";
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
                <button className="btn btn-primary btn-outline">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                  </svg>
                </button> 
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