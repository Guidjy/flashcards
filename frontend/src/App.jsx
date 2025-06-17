import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
// pages
import Home from './pages/Home'
import Auth from './pages/Auth'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Router>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/auth' element={<Auth />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
