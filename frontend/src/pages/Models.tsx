import { useEffect, useState } from 'react'
import { get, post } from '@/api/client'

type Model = { id: number; name: string; type: string; framework: string; accuracy: number }

export default function Models() {
  const [models, setModels] = useState<Model[]>([])
  const [name, setName] = useState('')
  const [type, setType] = useState('classification')

  async function load() {
    const data = await get<Model[]>('/models')
    setModels(data)
  }
  useEffect(() => { load() }, [])

  async function create() {
    if (!name) return
    await post('/models', { name, type, framework: 'pytorch', parameters: {} })
    setName('')
    load()
  }

  return (
    <div>
      <h3>Models</h3>
      <div style={{ display:'flex', gap:8, margin:'8px 0' }}>
        <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
        <select value={type} onChange={e => setType(e.target.value)}>
          <option value="classification">classification</option>
          <option value="detection">detection</option>
          <option value="segmentation">segmentation</option>
        </select>
        <button onClick={create}>Create</button>
      </div>
      <table cellPadding={8}>
        <thead><tr><th>ID</th><th>Name</th><th>Type</th><th>Framework</th><th>Accuracy</th></tr></thead>
        <tbody>
          {models.map(m => (
            <tr key={m.id}><td>{m.id}</td><td>{m.name}</td><td>{m.type}</td><td>{m.framework}</td><td>{m.accuracy}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}


