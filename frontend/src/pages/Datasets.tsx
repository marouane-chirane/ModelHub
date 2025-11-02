import { useEffect, useState } from 'react'
import { get, post } from '@/api/client'

type Dataset = { id: number; name: string; description?: string }

export default function Datasets() {
  const [items, setItems] = useState<Dataset[]>([])
  const [name, setName] = useState('')
  const [desc, setDesc] = useState('')

  async function load() {
    const data = await get<Dataset[]>('/datasets')
    setItems(data)
  }

  useEffect(() => {
    load()
  }, [])

  async function create() {
    if (!name) return
    await post<Dataset>('/datasets', { name, description: desc })
    setName('')
    setDesc('')
    load()
  }

  return (
    <div>
      <h3>Datasets</h3>
      <div style={{ display: 'flex', gap: 8, margin: '8px 0' }}>
        <input placeholder="Nom" value={name} onChange={e => setName(e.target.value)} />
        <input placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)} />
        <button onClick={create}>Créer</button>
      </div>
      <table cellPadding={8}>
        <thead>
          <tr><th>ID</th><th>Nom</th><th>Description</th></tr>
        </thead>
        <tbody>
          {items.map(d => (
            <tr key={d.id}><td>{d.id}</td><td>{d.name}</td><td>{d.description}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}


