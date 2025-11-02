from typing import Dict, Any
from app.pipelines.registry import create_pipeline
from app.pipelines.base import Pipeline, PipelineContext


def run_pipeline(kind: str, config: Dict[str, Any]) -> Dict[str, Any]:
	pipeline: Pipeline = create_pipeline(kind, config)
	ctx = PipelineContext()
	ctx = pipeline.run(ctx)
	return {
		"name": pipeline.name,
		"status": pipeline.status,
		"steps": [
			{
				"name": s.name,
				"status": s.status,
				"started_at": s.started_at,
				"finished_at": s.finished_at,
				"message": s.message,
			}
			for s in pipeline.steps
		],
		"metrics": ctx.metrics,
	}

