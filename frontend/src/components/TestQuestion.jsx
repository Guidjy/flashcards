export default function TestQuestion({ question, choices, answer }) {
  return (
    <>
      <h1 className="mb-2">{question}</h1>
      <ol className="space-y-1">
        {choices.map((choice, index) => {
          // gets the unicode character for a, b, c, d
          const letter = String.fromCharCode(97 + index).toUpperCase();
          if (letter === answer) console.log(answer);
          return (
            <li key={index}>
              {/*had to add justify-start here so that the text would align to the left*/}
              <button className="btn w-full justify-start text-left">
                <strong>{letter})</strong> {choice}
              </button>
            </li>
          );
        })}
      </ol>
      <h1>{answer}</h1>
    </>
  )
}