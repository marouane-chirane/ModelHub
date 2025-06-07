from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.deep_learning import (
    DeepLearningModelCreate,
    DeepLearningModelUpdate,
    DeepLearningModelInDB
)
from app.services.deep_learning import DeepLearningService

router = APIRouter()

@router.post("/", response_model=DeepLearningModelInDB)
def create_model(
    *,
    db: Session = Depends(deps.get_db),
    model_in: DeepLearningModelCreate
):
    """Crée un nouveau modèle de deep learning."""
    service = DeepLearningService(db)
    return service.create_model(model_in)

@router.get("/{model_id}", response_model=DeepLearningModelInDB)
def get_model(
    model_id: int,
    db: Session = Depends(deps.get_db)
):
    """Récupère un modèle par son ID."""
    service = DeepLearningService(db)
    model = service.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    return model

@router.put("/{model_id}", response_model=DeepLearningModelInDB)
def update_model(
    *,
    db: Session = Depends(deps.get_db),
    model_id: int,
    model_in: DeepLearningModelUpdate
):
    """Met à jour un modèle existant."""
    service = DeepLearningService(db)
    model = service.update_model(model_id, model_in)
    if not model:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    return model

@router.get("/", response_model=List[DeepLearningModelInDB])
def list_models(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    model_type: Optional[str] = None,
    status: Optional[str] = None,
    min_accuracy: Optional[float] = None,
    max_accuracy: Optional[float] = None
):
    """Liste tous les modèles avec filtres optionnels."""
    service = DeepLearningService(db)
    
    if model_type:
        return service.get_by_type(model_type)
    elif status:
        return service.get_by_status(status)
    elif min_accuracy is not None and max_accuracy is not None:
        return service.get_by_accuracy_range(min_accuracy, max_accuracy)
    else:
        return service.get_multi(skip=skip, limit=limit)

@router.delete("/{model_id}")
def delete_model(
    model_id: int,
    db: Session = Depends(deps.get_db)
):
    """Supprime un modèle."""
    service = DeepLearningService(db)
    model = service.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    service.remove(model_id)
    return {"status": "success"} 