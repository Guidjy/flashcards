export default function FlashCard({front, back, image}) {
  return (
    <>
      <h1 className="text-2xl md:text-3xl">{front}</h1>
      <div className="divider"></div>
      <p className="text-md md:text-lg">{back}</p>
      {image && (
        <img src={image} alt="Card illustration" />
      )}
    </>
  )
}