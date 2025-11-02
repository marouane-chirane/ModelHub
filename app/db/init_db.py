from sqlalchemy.orm import Session
from app.db.base_class import Base
from app.db.session import engine, SessionLocal
from app.models.ml_models import MLModel
from app.models.dl_models import DLModel
from app.models.user import User
from app.models.dataset import Dataset, ImageAsset, Annotation
from app.core.security import get_password_hash, generate_uuid


def init_db() -> None:
    """Initialize the database."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
		# Ensure admin user exists
        admin = db.query(User).filter(User.email == "admin@modelhub.com").first()
        if not admin:
            admin = User(
                id=generate_uuid(),
                email="admin@modelhub.com",
                username="admin",
				hashed_password=get_password_hash("admin123"),
                is_superuser=True,
            )
            db.add(admin)
            db.commit()
			db.refresh(admin)
        
		# Seed example DL model if empty
		if db.query(DLModel).first() is None:
			seed_dl = [
				DLModel(
					name="Simple CNN",
					type="classification",
					architecture="resnet18",
					parameters={"lr": 0.001},
					accuracy=0.0,
				),
			]
			for m in seed_dl:
				db.add(m)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()


def init_test_data(db: Session) -> None:
    """Initialise des données de test."""
    # TODO: Ajouter des données de test si nécessaire
    pass 