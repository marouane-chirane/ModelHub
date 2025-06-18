from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.time_series_training import TimeSeriesTrainer
import pandas as pd
from typing import Dict, Any
import json

router = APIRouter()
trainer = TimeSeriesTrainer()

@router.post("/upload")
async def upload_time_series_data(
    file: UploadFile = File(...),
    target_column: str = None
):
    """Upload time series data"""
    try:
        # Read CSV file
        df = pd.read_csv(file.file)
        
        # Validate target column
        if target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target column '{target_column}' not found in data")
        
        # Store data in session or temporary storage
        # In a real application, you might want to store this in a database or file system
        return {"message": "Data uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/train")
async def train_time_series_model(config: Dict[str, Any]):
    """Train a time series model"""
    try:
        # Get model type and parameters
        model_type = config.get("type")
        parameters = config.get("parameters", {})
        forecast_horizon = config.get("forecast_horizon", 12)
        validation_split = config.get("validation_split", 0.2)
        
        # Train model based on type
        if model_type == "arima":
            model = trainer.train_arima(
                data=parameters.get("data"),
                order=tuple(parameters.get("order", (1,1,1)))
            )
        elif model_type == "sarima":
            model = trainer.train_sarima(
                data=parameters.get("data"),
                order=tuple(parameters.get("order", (1,1,1))),
                seasonal_order=tuple(parameters.get("seasonal_order", (1,1,1,12)))
            )
        elif model_type == "prophet":
            model = trainer.train_prophet(
                data=parameters.get("data"),
                seasonality_mode=parameters.get("seasonality_mode", "additive")
            )
        elif model_type == "lstm":
            model = trainer.train_lstm(
                data=parameters.get("data"),
                sequence_length=parameters.get("sequence_length", 10),
                epochs=parameters.get("epochs", 50)
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported model type: {model_type}")
        
        # Evaluate model
        metrics = trainer.evaluate_model(
            model=model,
            test_data=parameters.get("test_data"),
            model_type=model_type
        )
        
        # Save model
        model_data = {
            "name": f"{model_type}_model",
            "type": model_type,
            "parameters": parameters,
            "metrics": metrics,
            "forecast_horizon": forecast_horizon,
            "validation_split": validation_split
        }
        saved_model = trainer.save_model(model_data)
        
        return {
            "model_id": saved_model.id,
            "metrics": metrics,
            "plot": {
                "dates": parameters.get("dates").tolist(),
                "actual": parameters.get("actual").tolist(),
                "predicted": parameters.get("predicted").tolist()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_time_series_models():
    """Get all time series models"""
    try:
        # In a real application, fetch from database
        return {"models": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}")
async def get_time_series_model(model_id: int):
    """Get a specific time series model"""
    try:
        # In a real application, fetch from database
        return {"model": {}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 