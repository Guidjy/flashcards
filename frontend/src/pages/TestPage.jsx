// layout
import MainLayout from "../layouts/MainLayout";
// hooks
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
// services
import api from "../services/makeRequestWithAuth";

export default function TestPage() {
  const { deckId, nQuestions } = useParams();
  const [loading, setLoading] = useState(false);
  const [test, setTest] = useState({});

  useEffect(() => {
    async function takeTest() {
      setLoading(true);
      const response = await api.get(`take-test/${deckId}/${nQuestions}`);
      setTest(response.data);
      setLoading(false);
      console.log(response.data);
    }
    takeTest();
  }, [deckId, nQuestions]);

  return (
    <>
      {loading}
    </>
  );
}
