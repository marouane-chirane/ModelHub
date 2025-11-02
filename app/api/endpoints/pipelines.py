from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.pipeline_runner import run_pipeline

router = APIRouter()

@router.post("/run")
def run(req: Dict[str, Any]):
	"""Run a pipeline synchronously (demo)."""
	kind = req.get("kind")
	config = req.get("config", {})
	if not kind:
		raise HTTPException(status_code=400, detail="Missing 'kind'")
	result = run_pipeline(kind, config)
	return result

