from fastapi import FastAPI
from app.api.endpoints import models, time_series

app = FastAPI(
    title="ModelHub API",
    description="API pour la gestion et l'entraînement de modèles de machine learning",
    version="1.0.0"
)

# Inclusion des routes API
app.include_router(models.router, prefix="/api/v1", tags=["models"])
app.include_router(time_series.router, prefix="/api/v1/time-series", tags=["time-series"])

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "ModelHub API",
        "version": "1.0.0",
        "endpoints": {
            "models": "/api/v1/models",
            "time_series": "/api/v1/time-series",
            "docs": "/docs"
        }
    } 