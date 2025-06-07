from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.deep_learning import DeepLearningModel
from app.schemas.deep_learning import DeepLearningModelCreate, DeepLearningModelUpdate
from app.services.base import BaseService

class DeepLearningService(BaseService[DeepLearningModel]):
    def __init__(self, db: Session):
        super().__init__(DeepLearningModel, db)

    def create_model(self, model: DeepLearningModelCreate) -> DeepLearningModel:
        """Crée un nouveau modèle de deep learning."""
        db_model = DeepLearningModel(**model.dict())
        self.db.add(db_model)
        self.db.commit()
        self.db.refresh(db_model)
        return db_model

    def update_model(self, model_id: int, 
                    model: DeepLearningModelUpdate) -> Optional[DeepLearningModel]:
        """Met à jour un modèle existant."""
        db_model = self.get(model_id)
        if not db_model:
            return None
        
        for field, value in model.dict(exclude_unset=True).items():
            setattr(db_model, field, value)
        
        self.db.commit()
        self.db.refresh(db_model)
        return db_model

    def get_by_type(self, model_type: str) -> List[DeepLearningModel]:
        """Récupère tous les modèles d'un type donné."""
        return self.db.query(DeepLearningModel).filter(
            DeepLearningModel.model_type == model_type
        ).all()

    def get_by_status(self, status: str) -> List[DeepLearningModel]:
        """Récupère tous les modèles avec un statut donné."""
        return self.db.query(DeepLearningModel).filter(
            DeepLearningModel.status == status
        ).all()

    def get_by_accuracy_range(self, min_accuracy: float, 
                            max_accuracy: float) -> List[DeepLearningModel]:
        """Récupère tous les modèles dans une plage de précision donnée."""
        return self.db.query(DeepLearningModel).filter(
            DeepLearningModel.accuracy >= min_accuracy,
            DeepLearningModel.accuracy <= max_accuracy
        ).all()

    def update_weights(self, model_id: int, weights_path: str) -> Optional[DeepLearningModel]:
        """Met à jour le chemin des poids du modèle."""
        db_model = self.get(model_id)
        if not db_model:
            return None
        
        db_model.weights_path = weights_path
        self.db.commit()
        self.db.refresh(db_model)
        return db_model 