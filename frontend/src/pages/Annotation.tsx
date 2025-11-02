import { useEffect, useMemo, useState } from 'react'
import { get, post } from '@/api/client'

type Dataset = { id: number; name: string }
type Image = { id: number; dataset_id: number; path: string }

export default function Annotation() {
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [datasetId, setDatasetId] = useState<number | null>(null)
  const [images, setImages] = useState<Image[]>([])
  const [imgId, setImgId] = useState<number | null>(null)
  const [imgPath, setImgPath] = useState('')
  const [label, setLabel] = useState('')
  const [rect, setRect] = useState({ x: 0.1, y: 0.1, w: 0.3, h: 0.3 })

  useEffect(() => { (async () => {
    const ds = await get<Dataset[]>('/datasets');
    setDatasets(ds)
    if (ds[0]) setDatasetId(ds[0].id)
  })() }, [])

  useEffect(() => { (async () => {
    if (!datasetId) return
    const ims = await get<Image[]>(`/datasets/${datasetId}/images`)
    setImages(ims)
    if (ims[0]) setImgId(ims[0].id)
  })() }, [datasetId])

  const selectedImage = useMemo(() => images.find(i => i.id === imgId), [images, imgId])

  async function addImage() {
    if (!datasetId || !imgPath) return
    await post('/images', { dataset_id: datasetId, path: imgPath })
    setImgPath('')
    const ims = await get<Image[]>(`/datasets/${datasetId}/images`)
    setImages(ims)
  }

  async function saveAnnotation() {
    if (!imgId || !label) return
    await post('/annotations', { image_id: imgId, label, ...rect })
    alert('Annotation enregistrée')
  }

  return (
    <div>
      <h3>Annotation</h3>
      <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
        <select value={datasetId ?? ''} onChange={e => setDatasetId(Number(e.target.value))}>
          {datasets.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
        <input placeholder="Chemin absolu image" value={imgPath} onChange={e => setImgPath(e.target.value)} />
        <button onClick={addImage}>Ajouter image</button>
      </div>
      <div style={{ display: 'flex', gap: 16 }}>
        <div>
          <div style={{ marginBottom: 8 }}>
            <select value={imgId ?? ''} onChange={e => setImgId(Number(e.target.value))}>
              {images.map(i => <option key={i.id} value={i.id}>{i.path}</option>)}
            </select>
          </div>
          <div style={{ position: 'relative', width: 640, height: 480, background: '#eee' }}>
            {/* Placeholder: background image not loaded for local fs security; draw rect overlay */}
            <div style={{ position:'absolute', left: rect.x*640, top: rect.y*480, width: rect.w*640, height: rect.h*480, border:'2px solid red', boxSizing:'border-box', background:'rgba(255,0,0,0.2)'}} />
          </div>
        </div>
        <div style={{ minWidth: 280 }}>
          <div>
            <label>Label</label>
            <input value={label} onChange={e => setLabel(e.target.value)} />
          </div>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:8, marginTop:8 }}>
            <label>x</label><input type="number" step="0.01" value={rect.x} onChange={e => setRect({ ...rect, x: Number(e.target.value) })} />
            <label>y</label><input type="number" step="0.01" value={rect.y} onChange={e => setRect({ ...rect, y: Number(e.target.value) })} />
            <label>w</label><input type="number" step="0.01" value={rect.w} onChange={e => setRect({ ...rect, w: Number(e.target.value) })} />
            <label>h</label><input type="number" step="0.01" value={rect.h} onChange={e => setRect({ ...rect, h: Number(e.target.value) })} />
          </div>
          <button style={{ marginTop: 12 }} onClick={saveAnnotation}>Enregistrer</button>
        </div>
      </div>
    </div>
  )
}


