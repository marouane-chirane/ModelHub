from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Créer le moteur de base de données
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 