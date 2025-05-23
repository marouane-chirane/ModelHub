from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.models.ml_model import MLModel
from app.models.ml_models.sklearn_model import SklearnModel
from app.models.dl_models.pytorch_model import PyTorchModel
from app.preprocessing.text.text_preprocessor import TextPreprocessor
from app.preprocessing.image.image_preprocessor import ImagePreprocessor
from app.api.dependencies import get_db
from pydantic import BaseModel

router = APIRouter()

class ModelCreate(BaseModel):
    name: str
    type: str
    framework: str
    description: Optional[str] = None
    hyperparameters: dict

class ModelResponse(BaseModel):
    id: int
    name: str
    type: str
    framework: str
    description: Optional[str]
    hyperparameters: dict
    metrics: Optional[dict]

    model_config = {
        "from_attributes": True
    }

@router.post("/models/", response_model=ModelResponse)
def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    """Crée un nouveau modèle."""
    db_model = MLModel(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.get("/models/", response_model=List[ModelResponse])
def list_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Liste tous les modèles."""
    models = db.query(MLModel).offset(skip).limit(limit).all()
    return models

@router.get("/models/{model_id}", response_model=ModelResponse)
def get_model(model_id: int, db: Session = Depends(get_db)):
    """Récupère un modèle spécifique."""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    return model

@router.post("/models/{model_id}/train")
def train_model(
    model_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Entraîne un modèle avec les données fournies."""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    # Créer l'instance du modèle approprié
    if model.framework == "sklearn":
        ml_model = SklearnModel(config={"hyperparameters": model.hyperparameters})
    elif model.framework == "pytorch":
        ml_model = PyTorchModel(config={"hyperparameters": model.hyperparameters})
    else:
        raise HTTPException(status_code=400, detail="Framework non supporté")
    
    # TODO: Charger et prétraiter les données
    # TODO: Entraîner le modèle
    # TODO: Sauvegarder le modèle entraîné
    
    return {"message": "Modèle entraîné avec succès"}

@router.post("/models/{model_id}/predict")
def predict(
    model_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Fait des prédictions avec un modèle entraîné."""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    # TODO: Charger le modèle
    # TODO: Prétraiter les données d'entrée
    # TODO: Faire des prédictions
    
    return {"predictions": []}

@router.delete("/models/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    """Supprime un modèle."""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    db.delete(model)
    db.commit()
    return {"message": "Modèle supprimé avec succès"} 