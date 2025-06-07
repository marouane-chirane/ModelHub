from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class DeepLearningModelBase(BaseModel):
    name: str
    description: Optional[str] = None
    model_type: str
    architecture: Dict[str, Any]
    hyperparameters: Optional[Dict[str, Any]] = None
    weights_path: Optional[str] = None
    version: Optional[str] = None
    accuracy: Optional[float] = None
    status: str = "draft"

class DeepLearningModelCreate(DeepLearningModelBase):
    pass

class DeepLearningModelUpdate(DeepLearningModelBase):
    name: Optional[str] = None
    model_type: Optional[str] = None
    architecture: Optional[Dict[str, Any]] = None

class DeepLearningModelInDB(DeepLearningModelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 