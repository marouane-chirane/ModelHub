import pytest
from app.services.training import ModelTrainer
from app.services.evaluation import ModelEvaluator
from app.models.ml_models import MLModel
from app.models.dl_models import DLModel
import numpy as np

@pytest.fixture
def sample_data():
    """Fixture pour les données de test"""
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)
    return X, y

def test_model_trainer_ml(sample_data):
    """Test l'entraînement d'un modèle ML"""
    X, y = sample_data
    trainer = ModelTrainer()
    
    # Test avec un modèle de classification
    model = trainer.train_ml_model(
        X=X,
        y=y,
        model_type="classification",
        parameters={"max_depth": 3}
    )
    
    assert model is not None
    assert hasattr(model, "predict")
    assert hasattr(model, "score")

def test_model_trainer_dl(sample_data):
    """Test l'entraînement d'un modèle DL"""
    X, y = sample_data
    trainer = ModelTrainer()
    
    # Test avec un modèle CNN
    model = trainer.train_dl_model(
        X=X,
        y=y,
        model_type="cnn",
        parameters={"learning_rate": 0.001}
    )
    
    assert model is not None
    assert hasattr(model, "predict")
    assert hasattr(model, "evaluate")

def test_model_evaluator(sample_data):
    """Test l'évaluation d'un modèle"""
    X, y = sample_data
    evaluator = ModelEvaluator()
    
    # Créer un modèle simple pour le test
    trainer = ModelTrainer()
    model = trainer.train_ml_model(X, y, "classification")
    
    # Évaluer le modèle
    metrics = evaluator.evaluate_model(model, X, y)
    
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert all(0 <= v <= 1 for v in metrics.values())

def test_invalid_model_type():
    """Test avec un type de modèle invalide"""
    trainer = ModelTrainer()
    with pytest.raises(ValueError):
        trainer.train_ml_model(
            X=np.random.rand(10, 5),
            y=np.random.randint(0, 2, 10),
            model_type="invalid_type"
        ) 