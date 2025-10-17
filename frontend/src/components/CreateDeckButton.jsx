// components
import { Form } from "./Form"
// hooks
import { useState } from "react";
// serivces
import { deckCreate } from "../services/decks";


export default function CreateDeckButton({ onDeckCreate }) {

  const [deckName, setDeckName] = useState("");

  const fields = [
    { label: "Name", type: "text", placeholder: "deck name", onChange: (event) => {setDeckName(event.target.value)} },
  ];


  return (
    <>
      {/*Button*/}
      <button className="btn btn-primary btn-outline rounded-3xl mt-2 w-1/3 lg:w-1/4 text-sm lg:text-md" onClick={()=>document.getElementById('my_modal_2').showModal()}>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
        </svg> | Create Deck
      </button>
      {/*Modal*/}
      <dialog id="my_modal_2" className="modal">
        <div className="modal-box">
          <div className="w-full flex justify-center">
            <Form 
              title="Create Deck" 
              fields={fields} 
              buttonText="Create"
              onSubmit={async () => {await deckCreate(deckName); onDeckCreate();}}
            />
          </div>
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </>
  )
}