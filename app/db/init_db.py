from sqlalchemy.orm import Session
from app.models.base import Base
from app.db.session import engine, SessionLocal
from app.models.ml_model import MLModel

def init_db() -> None:
    """Initialise la base de données."""
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # Vérifier si des modèles existent déjà
        if db.query(MLModel).first() is None:
            # Créer des modèles de test
            test_models = [
                MLModel(
                    name="Random Forest Classifier",
                    type="Classification",
                    framework="sklearn",
                    description="Classificateur Random Forest pour la classification binaire",
                    hyperparameters={
                        "n_estimators": 100,
                        "max_depth": 10
                    }
                ),
                MLModel(
                    name="Neural Network",
                    type="Classification",
                    framework="pytorch",
                    description="Réseau de neurones pour la classification d'images",
                    hyperparameters={
                        "hidden_layers": [128, 64],
                        "learning_rate": 0.001
                    }
                )
            ]
            
            # Ajouter les modèles à la base de données
            for model in test_models:
                db.add(model)
            
            # Sauvegarder les changements
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

def init_test_data(db: Session) -> None:
    """Initialise des données de test."""
    # TODO: Ajouter des données de test si nécessaire
    pass 