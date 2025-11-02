import { useEffect, useState } from 'react'
import { get, post } from '@/api/client'

type Dataset = { id: number; name: string; description?: string }

export default function Datasets() {
  const [items, setItems] = useState<Dataset[]>([])
  const [name, setName] = useState('')
  const [desc, setDesc] = useState('')
  const [error, setError] = useState<string>('')
  const [loading, setLoading] = useState(false)

  async function load() {
    try {
      setError('')
      const data = await get<Dataset[]>('/datasets')
      setItems(data || [])
    } catch (err: any) {
      setError(`Erreur lors du chargement: ${err.message || 'Erreur inconnue'}`)
      console.error('Erreur load:', err)
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function create() {
    if (!name.trim()) {
      setError('Le nom du dataset est requis')
      return
    }
    
    setLoading(true)
    setError('')
    
    try {
      await post<Dataset>('/datasets', { name: name.trim(), description: desc || null })
      setName('')
      setDesc('')
      await load()
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Erreur lors de la création'
      setError(`Erreur: ${msg}`)
      console.error('Erreur create:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
      <h2 style={{ marginBottom: '1rem' }}>📂 Datasets</h2>
      {error && (
        <div style={{ 
          padding: '0.75rem', 
          marginBottom: '1rem', 
          background: '#fee', 
          color: '#c33', 
          borderRadius: '4px',
          border: '1px solid #fcc'
        }}>
          {error}
        </div>
      )}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        <input 
          placeholder="Nom du dataset" 
          value={name} 
          onChange={e => setName(e.target.value)}
          style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd', flex: '1', minWidth: '200px' }}
        />
        <input 
          placeholder="Description" 
          value={desc} 
          onChange={e => setDesc(e.target.value)}
          style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd', flex: '1', minWidth: '200px' }}
        />
        <button 
          onClick={create}
          disabled={loading}
          style={{ 
            padding: '0.5rem 1.5rem', 
            borderRadius: '4px', 
            border: 'none', 
            background: loading ? '#95a5a6' : '#3498db', 
            color: 'white', 
            cursor: loading ? 'wait' : 'pointer', 
            fontWeight: 'bold',
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? 'Création...' : 'Créer'}
        </button>
      </div>
      {items.length > 0 ? (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f8f9fa' }}>
              <th style={{ padding: '0.75rem', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>ID</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Nom</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Description</th>
            </tr>
          </thead>
          <tbody>
            {items.map(d => (
              <tr key={d.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                <td style={{ padding: '0.75rem' }}>{d.id}</td>
                <td style={{ padding: '0.75rem', fontWeight: '500' }}>{d.name}</td>
                <td style={{ padding: '0.75rem', color: '#6c757d' }}>{d.description || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p style={{ color: '#6c757d', textAlign: 'center', padding: '2rem' }}>Aucun dataset. Créez-en un nouveau !</p>
      )}
    </div>
  )
}


