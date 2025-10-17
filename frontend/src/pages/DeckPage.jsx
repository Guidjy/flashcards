// layout
import MainLayout from "../layouts/MainLayout";
// components
import { Link } from "react-router-dom";
// hooks
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
// services
import { deckGet } from "../services/decks";
import { viewDeckStats } from "../services/activities";
// assets
import geminiIcon from "../assets/google-gemini-icon.png";


export default function DeckPage() {
  

  const [deck, setDeck] = useState({});
  const [deckStats, setDeckStats] = useState();
  
  const { deckId } = useParams();

  useEffect(() => {

    async function fetchDeck(id) {
      const response = await deckGet(id);
      setDeck(response);
    }
    fetchDeck(deckId);

    async function fetchDeckStats(id) {
      const response = await viewDeckStats(id);
      setDeckStats(response.stats);
    }
    fetchDeckStats(deckId);

  }, [deckId])


  return (
    <>
      <MainLayout>
        <div className="bg-base-100 rounded-2xl p-5 flex flex-col items-center">
          <h1 className="text-5xl font-bold text-center mb-5">{deck.name}</h1>

          {/*stats*/}
          <div className="w-full flex justify-center mb-10">
            <div className="stats shadow">
              <div className="stat">
                <div className="stat-figure text-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6 inline-block h-8 w-8 stroke-current" >
                    <path strokeLinecap="round" strokeLinejoin="round" d="m10.5 21 5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 0 1 6-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 0 1-3.827-5.802" />
                  </svg>
                </div>
                <div className="stat-title">Total cards</div>
                <div className="stat-value text-primary">{deck.card_count}</div>
                 <div className="stat-desc">
                  <Link className="link link-info" to={`/add-cards/${deckId}`}>
                    Add Cards
                  </Link>
                </div>
              </div>
            </div>
          </div>
          <img className="h-90 mb-10" src={deckStats}></img>
          
          <Link to={`/study/${deckId}`} className="w-2/3">
            <button className="btn btn-primary w-full mb-5">Study Cards</button>
          </Link>
          <Link to={`/take-test/${deckId}/5 `} className="w-2/3">
            <div className="indicator w-full">
              <div className="indicator-item bg-warning rounded-full px-2">
                <img src={geminiIcon} className="h-5" alt="Gemini Icon" />
              </div>
              <button className="btn btn-secondary w-full">Take Test</button>
            </div>
          </Link>

        </div>
        
      </MainLayout>
    </>
  );
}