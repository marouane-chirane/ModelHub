from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router

app = FastAPI(
    title="ModelHub",
    description="Plateforme de Computer Vision",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "ModelHub API - Computer Vision Platform",
        "version": "1.0.0",
        "endpoints": {
            "models": "/api/v1/models",
            "datasets": "/api/v1/datasets",
            "pipelines": "/api/v1/pipelines",
            "docs": "/docs"
        }
    } 