import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Analyze from './pages/Analyze'
import './index.css'

function App() {
  return (
    <div className="app-container">
      <nav className="navbar">
        <Link to="/" className="logo" style={{ textDecoration: 'none', color: 'inherit' }}>
          Interview Post-Mortem
        </Link>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyze" element={<Analyze />} />
        </Routes>
      </main>

      <footer className="footer">
        <p>This tool provides guidance based on common hiring patterns. It does not represent official employer feedback.</p>
      </footer>
    </div>
  )
}

export default App
