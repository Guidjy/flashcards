export default function Card({ front, back, image }) {
return (
  <div className="card bg-base-100 w-96 shadow-sm">
  <figure>
    <img src={image}/>
  </figure>
  <div className="card-body">
    <h2 className="card-title">{front}</h2>
    <p>{back}</p>
    <div className="card-actions justify-end">
    </div>
  </div>
  </div>
)
}