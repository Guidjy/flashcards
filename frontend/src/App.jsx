// React
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
// stles
import './styles/App.css'
// pages
import HomePage from './pages/HomePage'
import DeckPage from './pages/DeckPage'
import CreateCardPage from './pages/CreateCardPage'
import StudyPage from './pages/StudyPage'
import DeckShopPage from './pages/DeckShopPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import TestPage from './pages/TestPage'

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/deck/:deckId' element={<DeckPage />} />
          <Route path='/deck/:deckId/add-cards' element={<CreateCardPage />} />
          <Route path='/study/:deckId' element={<StudyPage />} />
          <Route path='/deck-shop/' element={<DeckShopPage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/register' element={<RegisterPage />} />
          <Route path='/take-test/:deckId/:nQuestions' element={<TestPage />} />
        </Routes>
      </Router>
    </>
  )
}

export default App