// components
import { Form } from "./Form";
// hooks
import { useState } from "react";
// services
import { deckPatch, deckDelete } from "../services/decks";


export default function EditDeckButton({ deckId, onDeckCreate }) {

  const [deckName, setDeckName] = useState("");

  const fields = [
    { label: "Name", type: "text", placeholder: "deck name", onChange: (event) => {setDeckName(event.target.value)} },
  ]
  
  return (
    <>
    <button className="btn btn-primary btn-outline" onClick={()=>document.getElementById(`my_modal_${deckId}`).showModal()}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
        <path strokeLinecap="round" strokeLinejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
      </svg>
    </button>

    {/* edit form */}
    <dialog id={`my_modal_${deckId}`} className="modal">
      <div className="modal-box">
        <div className="w-full flex flex-col items-center">
          <div className="w-full flex justify-center">
            <Form 
              title="Edit Deck" 
              fields={fields} 
              buttonText="Edit"
              onSubmit={async () => {await deckPatch(deckId, {name: deckName}); onDeckCreate();}}
            />
          </div>
          <button 
            className="btn btn-error w-4/5 mt-5" 
            onClick={async () => {await deckDelete(deckId); onDeckCreate();}}
          >
            Delete
          </button>
        </div>
      </div>
      <form method="dialog" className="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
    </>
  )
}