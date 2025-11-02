from fastapi import APIRouter, UploadFile, File
from typing import Dict, Any

router = APIRouter()

@router.post("/predict")
async def predict(task: str, file: UploadFile = File(...)) -> Dict[str, Any]:
	# TODO: Load model artifact from registry/storage based on task/model_id
	# For now, return a stubbed prediction
	return {
		"task": task,
		"prediction": [
			{"label": "demo", "score": 0.99}
		]
	}

