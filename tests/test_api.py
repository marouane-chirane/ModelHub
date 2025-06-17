from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.db.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import get_db

# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    
    Base.metadata.drop_all(bind=engine)

def test_create_model(client):
    """Test la création d'un modèle via l'API"""
    response = client.post(
        "/api/v1/models/",
        json={
            "name": "Test Model",
            "type": "classification",
            "parameters": {"max_depth": 5},
            "accuracy": 0.95
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Model"
    assert data["type"] == "classification"

def test_get_models(client):
    """Test la récupération des modèles"""
    # Créer d'abord un modèle
    client.post(
        "/api/v1/models/",
        json={
            "name": "Test Model",
            "type": "classification",
            "parameters": {"max_depth": 5},
            "accuracy": 0.95
        }
    )
    
    # Récupérer tous les modèles
    response = client.get("/api/v1/models/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Model"

def test_get_model_by_id(client):
    """Test la récupération d'un modèle par son ID"""
    # Créer un modèle
    create_response = client.post(
        "/api/v1/models/",
        json={
            "name": "Test Model",
            "type": "classification",
            "parameters": {"max_depth": 5},
            "accuracy": 0.95
        }
    )
    model_id = create_response.json()["id"]
    
    # Récupérer le modèle par son ID
    response = client.get(f"/api/v1/models/{model_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == model_id
    assert data["name"] == "Test Model"

def test_update_model(client):
    """Test la mise à jour d'un modèle"""
    # Créer un modèle
    create_response = client.post(
        "/api/v1/models/",
        json={
            "name": "Test Model",
            "type": "classification",
            "parameters": {"max_depth": 5},
            "accuracy": 0.95
        }
    )
    model_id = create_response.json()["id"]
    
    # Mettre à jour le modèle
    response = client.put(
        f"/api/v1/models/{model_id}",
        json={
            "name": "Updated Model",
            "type": "classification",
            "parameters": {"max_depth": 10},
            "accuracy": 0.98
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Model"
    assert data["parameters"]["max_depth"] == 10

def test_delete_model(client):
    """Test la suppression d'un modèle"""
    # Créer un modèle
    create_response = client.post(
        "/api/v1/models/",
        json={
            "name": "Test Model",
            "type": "classification",
            "parameters": {"max_depth": 5},
            "accuracy": 0.95
        }
    )
    model_id = create_response.json()["id"]
    
    # Supprimer le modèle
    response = client.delete(f"/api/v1/models/{model_id}")
    assert response.status_code == 200
    
    # Vérifier que le modèle n'existe plus
    get_response = client.get(f"/api/v1/models/{model_id}")
    assert get_response.status_code == 404 