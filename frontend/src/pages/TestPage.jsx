// layout
import MainLayout from "../layouts/MainLayout";
// hooks
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
// services
import api from "../services/makeRequestWithAuth";
// components
import TestQuestion from "../components/TestQuestion";


export default function TestPage() {
  const { deckId, nQuestions } = useParams();
  const [loading, setLoading] = useState(false);
  const [test, setTest] = useState([]);

  useEffect(() => {
    async function takeTest() {
      setLoading(true);
      const response = await api.get(`take-test/${deckId}/${nQuestions}`);
      setTest(response.data.test);
      setLoading(false);
    }
    takeTest();
  }, [deckId, nQuestions]);

  return (
    <>
      <div className="flex justify-center w-full bg-base-300 p-5">
        <div className="bg-base-100 p-5 md:p-10 min-h-screen w-full md:w-3/4 lg:w-1/2 rounded-3xl">
          {loading ? (
            <span className="loading loading-spinner text-primary"></span>
          ) : (
            test.map((question, index) => (
              {/* FIX TS */}
              <TestQuestion
                key={index}
                question={question.question}
                choices={[question.A, question.B, question.C, question.D]}
                answer={question.answer}
                number={index}
              />
              <div className="divider"></div>
            )
          ))
        }
        </div>
      </div>
    </>
  );
}
