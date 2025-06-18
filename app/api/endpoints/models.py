from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.ml_models import MLModel as MLModelDB
from app.models.dl_models import DLModel as DLModelDB
from app.schemas.model import ModelCreate, ModelUpdate, ModelResponse

router = APIRouter()

@router.get("/models", response_model=List[ModelResponse])
async def get_models(db: Session = Depends(get_db)):
    """Récupérer tous les modèles"""
    try:
        ml_models = db.query(MLModelDB).all()
        dl_models = db.query(DLModelDB).all()
        
        # Combiner les modèles
        all_models = []
        for model in ml_models:
            all_models.append({
                "id": model.id,
                "name": model.name,
                "type": model.type,
                "framework": "sklearn",
                "accuracy": model.accuracy,
                "created_at": model.created_at
            })
        
        for model in dl_models:
            all_models.append({
                "id": model.id,
                "name": model.name,
                "type": model.type,
                "framework": "pytorch",
                "accuracy": model.accuracy,
                "created_at": model.created_at
            })
        
        return all_models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models", response_model=ModelResponse)
async def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    """Créer un nouveau modèle"""
    try:
        if model.framework == "sklearn":
            db_model = MLModelDB(
                name=model.name,
                type=model.type,
                parameters=model.parameters,
                accuracy=0.0
            )
        else:
            db_model = DLModelDB(
                name=model.name,
                type=model.type,
                parameters=model.parameters,
                accuracy=0.0
            )
        
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        
        return {
            "id": db_model.id,
            "name": db_model.name,
            "type": db_model.type,
            "framework": model.framework,
            "accuracy": db_model.accuracy,
            "created_at": db_model.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}", response_model=ModelResponse)
async def get_model(model_id: int, db: Session = Depends(get_db)):
    """Récupérer un modèle spécifique"""
    try:
        # Chercher dans les modèles ML
        model = db.query(MLModelDB).filter(MLModelDB.id == model_id).first()
        if model:
            return {
                "id": model.id,
                "name": model.name,
                "type": model.type,
                "framework": "sklearn",
                "accuracy": model.accuracy,
                "created_at": model.created_at
            }
        
        # Chercher dans les modèles DL
        model = db.query(DLModelDB).filter(DLModelDB.id == model_id).first()
        if model:
            return {
                "id": model.id,
                "name": model.name,
                "type": model.type,
                "framework": "pytorch",
                "accuracy": model.accuracy,
                "created_at": model.created_at
            }
        
        raise HTTPException(status_code=404, detail="Model not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/models/{model_id}", response_model=ModelResponse)
async def update_model(model_id: int, model_update: ModelUpdate, db: Session = Depends(get_db)):
    """Mettre à jour un modèle"""
    try:
        # Chercher dans les modèles ML
        db_model = db.query(MLModelDB).filter(MLModelDB.id == model_id).first()
        if db_model:
            for field, value in model_update.dict(exclude_unset=True).items():
                setattr(db_model, field, value)
            db.commit()
            db.refresh(db_model)
            return {
                "id": db_model.id,
                "name": db_model.name,
                "type": db_model.type,
                "framework": "sklearn",
                "accuracy": db_model.accuracy,
                "created_at": db_model.created_at
            }
        
        # Chercher dans les modèles DL
        db_model = db.query(DLModelDB).filter(DLModelDB.id == model_id).first()
        if db_model:
            for field, value in model_update.dict(exclude_unset=True).items():
                setattr(db_model, field, value)
            db.commit()
            db.refresh(db_model)
            return {
                "id": db_model.id,
                "name": db_model.name,
                "type": db_model.type,
                "framework": "pytorch",
                "accuracy": db_model.accuracy,
                "created_at": db_model.created_at
            }
        
        raise HTTPException(status_code=404, detail="Model not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/models/{model_id}")
async def delete_model(model_id: int, db: Session = Depends(get_db)):
    """Supprimer un modèle"""
    try:
        # Chercher dans les modèles ML
        model = db.query(MLModelDB).filter(MLModelDB.id == model_id).first()
        if model:
            db.delete(model)
            db.commit()
            return {"message": "Model deleted successfully"}
        
        # Chercher dans les modèles DL
        model = db.query(DLModelDB).filter(DLModelDB.id == model_id).first()
        if model:
            db.delete(model)
            db.commit()
            return {"message": "Model deleted successfully"}
        
        raise HTTPException(status_code=404, detail="Model not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_id}/train")
def train_model(
    model_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Entraîne un modèle avec les données fournies."""
    model = db.query(MLModelDB).filter(MLModelDB.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    # TODO: Implémenter l'entraînement
    return {"message": "Modèle entraîné avec succès"}

@router.post("/models/{model_id}/predict")
def predict(
    model_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Fait des prédictions avec un modèle entraîné."""
    model = db.query(MLModelDB).filter(MLModelDB.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    # TODO: Implémenter les prédictions
    return {"predictions": []} 