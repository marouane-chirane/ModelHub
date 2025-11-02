import { useState } from 'react'
import { post } from '@/api/client'

export default function Pipelines() {
  const [kind, setKind] = useState('cv_classification')
  const [datasetPath, setDatasetPath] = useState('')
  const [epochs, setEpochs] = useState(1)
  const [trainRatio, setTrainRatio] = useState(0.8)
  const [lr, setLr] = useState(0.001)
  const [result, setResult] = useState<any>(null)

  async function run() {
    const data = await post('/pipelines/run', {
      kind,
      config: { dataset_path: datasetPath, epochs, train_ratio: trainRatio, lr }
    })
    setResult(data)
  }

  return (
    <div>
      <h3>Pipelines</h3>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:8, maxWidth:800 }}>
        <div>
          <label>Kind</label>
          <select value={kind} onChange={e => setKind(e.target.value)}>
            <option value="cv_classification">cv_classification</option>
            <option value="cv_detection">cv_detection</option>
            <option value="cv_segmentation">cv_segmentation</option>
          </select>
        </div>
        <div>
          <label>Dataset path</label>
          <input value={datasetPath} onChange={e => setDatasetPath(e.target.value)} placeholder="/abs/path/to/images" />
        </div>
        <div>
          <label>Epochs</label>
          <input type="number" value={epochs} onChange={e => setEpochs(Number(e.target.value))} />
        </div>
        <div>
          <label>Train ratio</label>
          <input type="number" step="0.01" value={trainRatio} onChange={e => setTrainRatio(Number(e.target.value))} />
        </div>
        <div>
          <label>LR</label>
          <input type="number" step="0.0001" value={lr} onChange={e => setLr(Number(e.target.value))} />
        </div>
      </div>
      <button style={{ marginTop: 12 }} onClick={run}>Run</button>
      {result && (
        <div style={{ marginTop: 16 }}>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}


