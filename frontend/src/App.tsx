import { Link, Route, Routes, Navigate } from 'react-router-dom'
import Datasets from '@/pages/Datasets'
import Annotation from '@/pages/Annotation'
import Pipelines from '@/pages/Pipelines'
import Models from '@/pages/Models'

export default function App() {
  return (
    <div style={{ fontFamily: 'Inter, system-ui, Arial', padding: 16 }}>
      <header style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 16 }}>
        <h2 style={{ marginRight: 16 }}>ModelHub CV</h2>
        <Link to="/datasets">Datasets</Link>
        <Link to="/annotation">Annotation</Link>
        <Link to="/pipelines">Pipelines</Link>
        <Link to="/models">Models</Link>
      </header>
      <Routes>
        <Route path="/" element={<Navigate to="/datasets" replace />} />
        <Route path="/datasets" element={<Datasets />} />
        <Route path="/annotation" element={<Annotation />} />
        <Route path="/pipelines" element={<Pipelines />} />
        <Route path="/models" element={<Models />} />
      </Routes>
    </div>
  )
}


