import { Link, Route, Routes, Navigate, useLocation } from 'react-router-dom'
import Datasets from '@/pages/Datasets'
import Annotation from '@/pages/Annotation'
import Pipelines from '@/pages/Pipelines'
import Models from '@/pages/Models'
import './App.css'

export default function App() {
  const location = useLocation()
  
  return (
    <div className="app">
      <header className="header">
        <h1 className="logo">🤖 ModelHub CV</h1>
        <nav className="nav">
          <Link 
            to="/datasets" 
            className={location.pathname === '/datasets' ? 'nav-link active' : 'nav-link'}
          >
            Datasets
          </Link>
          <Link 
            to="/annotation" 
            className={location.pathname === '/annotation' ? 'nav-link active' : 'nav-link'}
          >
            Annotation
          </Link>
          <Link 
            to="/pipelines" 
            className={location.pathname === '/pipelines' ? 'nav-link active' : 'nav-link'}
          >
            Pipelines
          </Link>
          <Link 
            to="/models" 
            className={location.pathname === '/models' ? 'nav-link active' : 'nav-link'}
          >
            Models
          </Link>
        </nav>
      </header>
      <main className="main">
        <Routes>
          <Route path="/" element={<Navigate to="/datasets" replace />} />
          <Route path="/datasets" element={<Datasets />} />
          <Route path="/annotation" element={<Annotation />} />
          <Route path="/pipelines" element={<Pipelines />} />
          <Route path="/models" element={<Models />} />
        </Routes>
      </main>
    </div>
  )
}


