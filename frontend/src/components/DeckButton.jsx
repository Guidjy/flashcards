import { Link } from "react-router-dom";


export default function DeckButton({ name, deck_id }) {
  return (
    <>
      <Link to={`deck/${deck_id}`}>
        <button className="btn w-full rounded-3xl">
          <p>{name}</p>
        </button>
      </Link>
    </>
  );
}