from typing import List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.dl_models import DLModel as DLModelDB
from app.schemas.model import ModelCreate, ModelUpdate, ModelResponse

router = APIRouter()

@router.get("/models", response_model=List[ModelResponse])
async def get_models(db: Session = Depends(get_db)):
	"""Récupérer tous les modèles (DL/CV uniquement)."""
    try:
        dl_models = db.query(DLModelDB).all()
		return [
			{
				"id": m.id,
				"name": m.name,
				"type": m.type,
                "framework": "pytorch",
				"accuracy": m.accuracy or 0.0,
				"created_at": m.created_at,
			}
			for m in dl_models
		]
	except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models", response_model=ModelResponse)
async def create_model(model: ModelCreate, db: Session = Depends(get_db)):
	"""Créer un nouveau modèle DL/CV."""
    try:
            db_model = DLModelDB(
                name=model.name,
                type=model.type,
                parameters=model.parameters,
			accuracy=0.0,
            )
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return {
            "id": db_model.id,
            "name": db_model.name,
            "type": db_model.type,
			"framework": "pytorch",
            "accuracy": db_model.accuracy,
			"created_at": db_model.created_at,
        }
	except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}", response_model=ModelResponse)
async def get_model(model_id: int, db: Session = Depends(get_db)):
	"""Récupérer un modèle spécifique DL/CV."""
	m = db.query(DLModelDB).filter(DLModelDB.id == model_id).first()
	if not m:
		raise HTTPException(status_code=404, detail="Model not found")
            return {
		"id": m.id,
		"name": m.name,
		"type": m.type,
                "framework": "pytorch",
		"accuracy": m.accuracy or 0.0,
		"created_at": m.created_at,
            }

@router.put("/models/{model_id}", response_model=ModelResponse)
async def update_model(model_id: int, model_update: ModelUpdate, db: Session = Depends(get_db)):
	"""Mettre à jour un modèle DL/CV."""
        db_model = db.query(DLModelDB).filter(DLModelDB.id == model_id).first()
	if not db_model:
		raise HTTPException(status_code=404, detail="Model not found")
            for field, value in model_update.dict(exclude_unset=True).items():
                setattr(db_model, field, value)
            db.commit()
            db.refresh(db_model)
            return {
                "id": db_model.id,
                "name": db_model.name,
                "type": db_model.type,
                "framework": "pytorch",
		"accuracy": db_model.accuracy or 0.0,
		"created_at": db_model.created_at,
            }

@router.delete("/models/{model_id}")
async def delete_model(model_id: int, db: Session = Depends(get_db)):
	"""Supprimer un modèle DL/CV."""
        model = db.query(DLModelDB).filter(DLModelDB.id == model_id).first()
	if not model:
		raise HTTPException(status_code=404, detail="Model not found")
            db.delete(model)
            db.commit()
            return {"message": "Model deleted successfully"}

@router.post("/models/{model_id}/train")
def train_model(
    model_id: int,
    file: UploadFile = File(...),
	db: Session = Depends(get_db),
):
	"""Entrainer un modèle DL/CV avec les données fournies (stub)."""
	model = db.query(DLModelDB).filter(DLModelDB.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
	# TODO: Implement training using pipeline
    return {"message": "Modèle entraîné avec succès"}

@router.post("/models/{model_id}/predict")
def predict(
    model_id: int,
    file: UploadFile = File(...),
	db: Session = Depends(get_db),
):
	"""Prédire avec un modèle DL/CV (stub)."""
	model = db.query(DLModelDB).filter(DLModelDB.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
	# TODO: Implement inference loading artifact
    return {"predictions": []} 