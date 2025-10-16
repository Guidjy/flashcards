import { useState } from "react";

export default function TestQuestion({ question, choices, answer, number }) {
  // letter of the answer that the user picked
  const [selected, setSelected] = useState(null);

  function onAnswer(choice) {
    if (selected) return;  // only allow one answer
    setSelected(choice);
  }

  return (
    <>
      <h1 className="mb-2">{number+1}) {question}</h1>
      <ol className="space-y-1">
        {choices.map((text, index) => {
          // gets letter from unicode
          const letter = String.fromCharCode(97 + index).toUpperCase();
          // decide button color based on selection and correctness
          let color = "btn w-full justify-start text-left";
          if (selected) {
            if (letter === answer) color += " btn-success";
            else if (letter === selected) color += " btn-error";
          }

          return (
            <li key={index}>
              <button className={color} onClick={() => onAnswer(letter)}>
                <strong>{letter})</strong> {text}
              </button>
            </li>
          );
        })}
      </ol>
    </>
  );
}
