// layout
import MainLayout from "../layouts/MainLayout";
// hooks
import { useParams } from "react-router-dom";
import { useState } from "react";
// components
import { Form } from "../components/Form";
// services
import { cardCreate } from "../services/cards";


export default function CreateCardPage() {
  
  const { deckId } = useParams();

  const [front, setFront] = useState("");
  const [back, setBack] = useState("");
  const [image, setImage] = useState(null);

  const fields = [
    { label: "Front", type: "text", placeholder: "front text", onChange: (event) => {setFront(event.target.value)} },
    { label: "Back", type: "text", placeholder: "back text", onChange: (event) => {setBack(event.target.value)} },
    { label: "Image", type: "file", placeholder: "", onChange: (event) => {setImage(event.target.files[0])} },
  ];

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
  }

  return (
    <MainLayout>
      <div className="bg-base-100 flex justify-center p-5 md:p-10 rounded-xl">
        <Form 
          title="Add Card"
          fields={fields}
          buttonText="Add Card"
          onSubmit={onFormSubmit}
        />
      </div>
    </MainLayout>
  )
}