// hooks
import { useState } from "react"


export default function FlashCard({front, back, image}) {

  const [backHidden, setBackHidden] = useState(true);


  return (
    <>
      <div className="flex flex-col items-center rounded-2xl bg-base-100 p-5 w-11/12 md:w-4/5 lg:w-1/2 h-11/12">
        <h1 className="text-2xl md:text-3xl">{front}</h1>
        <div className="divider"></div>
        {backHidden ? (
          <button className="btn btn-accent" onClick={() => setBackHidden(false)}>
            Show Answer
          </button>
        ) : (
          <CardBack back={back} image={image} />
        )}
      </div>
    </>
  )
}


function CardBack({ back, image }) {
  return (
    <>
      <p className="text-md md:text-lg mb-5">{back}</p>
      {image && (
        <div className="w-full h-full overflow-hidden flex items-center justify-center">
          <img
            src={image}
            alt="Card illustration"
            className="w-4/5 h-4/5 object-contain"
          />
        </div>
      )}
      
      <div className="w-full flex gap-4">
        <button className="btn btn-error flex-1">
          Fail
        </button>
        <button className="btn btn-success flex-1">
          Pass
        </button>
      </div>
    </>
  )
}