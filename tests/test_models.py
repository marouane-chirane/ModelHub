import pytest
from app.models.ml_models import MLModel
from app.models.dl_models import DLModel
from app.db.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_ml_model(db_session):
    """Test la création d'un modèle ML"""
    model = MLModel(
        name="Test Model",
        type="classification",
        parameters={"max_depth": 5},
        accuracy=0.95
    )
    db_session.add(model)
    db_session.commit()
    
    saved_model = db_session.query(MLModel).first()
    assert saved_model.name == "Test Model"
    assert saved_model.type == "classification"
    assert saved_model.parameters == {"max_depth": 5}
    assert saved_model.accuracy == 0.95

def test_create_dl_model(db_session):
    """Test la création d'un modèle DL"""
    model = DLModel(
        name="Test DL Model",
        type="cnn",
        architecture="resnet50",
        parameters={"learning_rate": 0.001},
        accuracy=0.92
    )
    db_session.add(model)
    db_session.commit()
    
    saved_model = db_session.query(DLModel).first()
    assert saved_model.name == "Test DL Model"
    assert saved_model.type == "cnn"
    assert saved_model.architecture == "resnet50"
    assert saved_model.parameters == {"learning_rate": 0.001}
    assert saved_model.accuracy == 0.92

def test_model_validation(db_session):
    """Test la validation des données du modèle"""
    with pytest.raises(ValueError):
        model = MLModel(
            name="",  # Nom vide
            type="invalid_type",  # Type invalide
            parameters={},
            accuracy=1.5  # Accuracy invalide
        )
        db_session.add(model)
        db_session.commit() 