from fastapi import APIRouter
from app.api.endpoints import models, auth, pipelines, serving, datasets

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include model routes
api_router.include_router(models.router, prefix="/models", tags=["models"]) 

# Include pipeline routes
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])

# Include serving routes
api_router.include_router(serving.router, prefix="/serve", tags=["serving"])

# Include dataset routes
api_router.include_router(datasets.router, tags=["datasets"]) 