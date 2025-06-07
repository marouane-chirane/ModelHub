from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class DeepLearningModel(Base):
    __tablename__ = "deep_learning_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    model_type = Column(String(50), nullable=False)  # CNN, RNN, Transformer, etc.
    architecture = Column(JSON, nullable=False)  # Model architecture configuration
    hyperparameters = Column(JSON)  # Training hyperparameters
    weights_path = Column(String(255))  # Path to model weights
    version = Column(String(20))
    accuracy = Column(Float)
    status = Column(String(20), default="draft")  # draft, training, ready, archived
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    predictions = relationship("Prediction", back_populates="model")
    training_runs = relationship("TrainingRun", back_populates="model") 