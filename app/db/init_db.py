from sqlalchemy.orm import Session
from app.models.base import Base
from app.db.session import engine, SessionLocal
from app.models.ml_model import MLModel
from app.models.user import User
from app.core.security import get_password_hash, generate_uuid

def init_db() -> None:
    """Initialize the database."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.email == "admin@modelhub.com").first()
        if not admin:
            admin = User(
                id=generate_uuid(),
                email="admin@modelhub.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),  # Change this in production!
                is_superuser=True,
            )
            db.add(admin)
            db.commit()
        
        # Check if models exist
        if db.query(MLModel).first() is None:
            # Create test models
            test_models = [
                MLModel(
                    name="Random Forest Classifier",
                    type="Classification",
                    framework="sklearn",
                    description="Random Forest Classifier for binary classification",
                    hyperparameters={
                        "n_estimators": 100,
                        "max_depth": 10
                    }
                ),
                MLModel(
                    name="Neural Network",
                    type="Classification",
                    framework="pytorch",
                    description="Neural Network for image classification",
                    hyperparameters={
                        "hidden_layers": [128, 64],
                        "learning_rate": 0.001
                    }
                )
            ]
            
            # Add models to database
            for model in test_models:
                db.add(model)
            
            # Save changes
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

def init_test_data(db: Session) -> None:
    """Initialise des données de test."""
    # TODO: Ajouter des données de test si nécessaire
    pass 