import { Link } from 'react-router-dom'
import { useEffect } from 'react'
import { userProfile } from '../services/userProfile'

export default function Navbar() {

  useEffect(() => {
    const profile = userProfile();
    console.log(profile);
  }, []);

  return (
    <div className="navbar bg-base-100 shadow-sm">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl">Flashcards</Link>
      </div>
      <div className="flex-none">
        <button className="btn btn-square btn-ghost">
          <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" className="bi bi-person-circle" viewBox="0 0 16 16">
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
            <path fillRule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
          </svg>
        </button>
        </div>
    </div>
  )
}