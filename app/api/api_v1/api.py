from fastapi import APIRouter
from app.api.endpoints import models, auth

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include model routes
api_router.include_router(models.router, prefix="/models", tags=["models"]) 