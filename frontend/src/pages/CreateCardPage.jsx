// layout
import MainLayout from "../layouts/MainLayout";
// hooks
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
// components
import { Form } from "../components/Form";
import Card from "../components/Card";
// services
import { cardCreate, cardsGetByDeckId } from "../services/cards";


export default function CreateCardPage() {
  
  const { deckId } = useParams();

  const [front, setFront] = useState("");
  const [back, setBack] = useState("");
  const [image, setImage] = useState(null);
  const [cards, setCards] = useState([]);
  const [cardCreated, setCardCreated] = useState(false);

  const fields = [
    { label: "Front", type: "text", placeholder: "front text", onChange: (event) => {setFront(event.target.value)} },
    { label: "Back", type: "text", placeholder: "back text", onChange: (event) => {setBack(event.target.value)} },
    { label: "Image", type: "file", placeholder: "", onChange: (event) => {setImage(event.target.files[0])} },
  ];


  // gets all of the cards from the current deck
  useEffect(() => {
    async function getCards(id) {
      const response = await cardsGetByDeckId(id);
      setCards(response);
    }
    getCards(deckId)
  }, [cardCreated]);


  async function onFormSubmit() {
    // https://developer.mozilla.org/en-US/docs/Web/API/FormData
    const formData = new FormData();
    formData.append('front', front);
    formData.append('back', back);
    formData.append('deck', deckId);
    if (image) {
      formData.append('image', image);
    }

    const response = await cardCreate(formData);
    console.log(response);

    setFront("");
    setBack("");
    setImage(null);
    setCardCreated(!cardCreated);
  }


  return (
    <MainLayout>
      <div className="bg-base-100 flex justify-center p-5 md:p-10 rounded-xl mb-10">
        <Form 
          title="Add Card"
          fields={fields}
          buttonText="Add Card"
          onSubmit={onFormSubmit}
        />
      </div>
    
      {/*Deck cards*/}
      <div className="bg-base-100 flex flex-col items-center p-5 md:p-10 rounded-xl">
        {cards.map((card, index) => (
          <div key={index}>
            <Card
              front={card.front}
              back={card.back}
              image={card.image}
            />
            <div className="divider"></div>
          </div>
        ))}
      </div>
    </MainLayout>
  )
}