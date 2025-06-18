from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ModelCreate(BaseModel):
    name: str
    type: str
    framework: str
    parameters: Dict[str, Any] = {}
    description: Optional[str] = None

class ModelUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    accuracy: Optional[float] = None
    description: Optional[str] = None

class ModelResponse(BaseModel):
    id: int
    name: str
    type: str
    framework: str
    accuracy: float
    created_at: datetime
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True 