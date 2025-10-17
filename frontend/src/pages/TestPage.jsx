// layout
import MainLayout from "../layouts/MainLayout";
// hooks
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
// services
import api from "../services/makeRequestWithAuth";
// components
import TestQuestion from "../components/TestQuestion";
import TestQuestionSkeleton from "../components/TestQuestionSkeleton";


export default function TestPage() {
  const { deckId, nQuestions } = useParams();
  const [loading, setLoading] = useState(false);
  const [test, setTest] = useState([]);

  const navigate = useNavigate();

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
    <MainLayout>
      <div className="bg-base-100 p-5 md:p-10 min-h-screen rounded-3xl">
        {loading ? (
          <>
            {/* FaceBook hates for loops so you have to do this bullshit to render the same component n times*/}
            {Array.from({ length: Number(nQuestions) }).map((question, index) => (
              <TestQuestionSkeleton key={index}/>
            ))}
          </>
        ) : (
          test.map((question, index) => (
            <>
              <TestQuestion
                key={index}
                question={question.question}
                choices={[question.A, question.B, question.C, question.D]}
                answer={question.answer}
                number={index}
              />
              <div className="divider"></div>
            </>
          )
        ))
      }
      <div className="flex justify-center w-full">
        <button className="btn btn-primary w-2/3" onClick={() => (navigate('/'))}>
          Finish Test
        </button>
      </div>
      </div>
    </MainLayout>
    </>
  );
}
