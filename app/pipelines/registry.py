from typing import Dict, Any
from app.pipelines.base import Pipeline, PipelineStep
from app.pipelines.steps_cv import (
	DataIngestionConfig,
	step_ingest_images,
	step_preprocess_images,
	step_split,
	step_train_classification,
	step_train_detection,
	step_train_segmentation,
	step_evaluate,
)


def build_cv_classification_pipeline(config: Dict[str, Any]) -> Pipeline:
	ingest = PipelineStep(
		name="ingest",
		func=step_ingest_images(
			DataIngestionConfig(dataset_path=config["dataset_path"])
		),
	)
	preprocess = PipelineStep(name="preprocess", func=step_preprocess_images())
	split = PipelineStep(name="split", func=step_split(config.get("train_ratio", 0.8)))
	train = PipelineStep(
		name="train",
		func=step_train_classification(
			model_name=config.get("model_name", "resnet18"),
			epochs=int(config.get("epochs", 1)),
			lr=float(config.get("lr", 1e-3)),
		),
	)
	eval_step = PipelineStep(name="evaluate", func=step_evaluate())
	return Pipeline(name="cv_classification", steps=[ingest, preprocess, split, train, eval_step])


def build_cv_detection_pipeline(config: Dict[str, Any]) -> Pipeline:
	ingest = PipelineStep(
		name="ingest",
		func=step_ingest_images(DataIngestionConfig(dataset_path=config["dataset_path"])),
	)
	preprocess = PipelineStep(name="preprocess", func=step_preprocess_images())
	split = PipelineStep(name="split", func=step_split(config.get("train_ratio", 0.8)))
	train = PipelineStep(
		name="train",
		func=step_train_detection(
			model_name=config.get("model_name", "fasterrcnn_resnet50_fpn"),
			epochs=int(config.get("epochs", 1)),
			lr=float(config.get("lr", 1e-3)),
		),
	)
	eval_step = PipelineStep(name="evaluate", func=step_evaluate())
	return Pipeline(name="cv_detection", steps=[ingest, preprocess, split, train, eval_step])


def build_cv_segmentation_pipeline(config: Dict[str, Any]) -> Pipeline:
	ingest = PipelineStep(
		name="ingest",
		func=step_ingest_images(DataIngestionConfig(dataset_path=config["dataset_path"])),
	)
	preprocess = PipelineStep(name="preprocess", func=step_preprocess_images())
	split = PipelineStep(name="split", func=step_split(config.get("train_ratio", 0.8)))
	train = PipelineStep(
		name="train",
		func=step_train_segmentation(
			model_name=config.get("model_name", "deeplabv3_resnet50"),
			epochs=int(config.get("epochs", 1)),
			lr=float(config.get("lr", 1e-3)),
		),
	)
	eval_step = PipelineStep(name="evaluate", func=step_evaluate())
	return Pipeline(name="cv_segmentation", steps=[ingest, preprocess, split, train, eval_step])


PIPELINE_BUILDERS = {
	"cv_classification": build_cv_classification_pipeline,
	"cv_detection": build_cv_detection_pipeline,
	"cv_segmentation": build_cv_segmentation_pipeline,
}


def create_pipeline(kind: str, config: Dict[str, Any]) -> Pipeline:
	if kind not in PIPELINE_BUILDERS:
		raise ValueError(f"Unknown pipeline kind: {kind}")
	return PIPELINE_BUILDERS[kind](config)
