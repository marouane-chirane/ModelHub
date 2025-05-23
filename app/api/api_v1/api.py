from fastapi import APIRouter
from app.api.endpoints import models

api_router = APIRouter()

# Inclure les routes des modèles
api_router.include_router(models.router, prefix="/models", tags=["models"]) 