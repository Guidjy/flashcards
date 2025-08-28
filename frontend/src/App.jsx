// React
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
// stles
import './styles/App.css'
// pages
import HomePage from './pages/HomePage'
import DeckPage from './pages/DeckPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/deck/:deckId' element={<DeckPage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/register' element={<RegisterPage />} />
        </Routes>
      </Router>
    </>
  )
}

export default App