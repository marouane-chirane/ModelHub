from typing import Any, Dict
from dataclasses import dataclass
import os

from app.pipelines.base import PipelineContext


@dataclass
class DataIngestionConfig:
	dataset_path: str


def step_ingest_images(config: DataIngestionConfig):
	def _fn(ctx: PipelineContext) -> PipelineContext:
		if not os.path.isdir(config.dataset_path):
			raise FileNotFoundError(f"Dataset path not found: {config.dataset_path}")
		ctx.data["images_path"] = config.dataset_path
		return ctx
	return _fn


def step_preprocess_images() -> Any:
	def _fn(ctx: PipelineContext) -> PipelineContext:
		# Placeholder: add resizing/normalization/augmentation hooks later
		ctx.artifacts["preprocessed"] = True
		return ctx
	return _fn


def step_split(train_ratio: float = 0.8):
	def _fn(ctx: PipelineContext) -> PipelineContext:
		# Placeholder: record split metadata
		ctx.data["split"] = {"train_ratio": train_ratio}
		return ctx
	return _fn


def step_train_classification(model_name: str = "resnet18", epochs: int = 1, lr: float = 1e-3):
	def _fn(ctx: PipelineContext) -> PipelineContext:
		# TODO: Implement training using torchvision/timm
		ctx.artifacts["model"] = {
			"task": "classification",
			"arch": model_name,
			"epochs": epochs,
			"lr": lr,
		}
		return ctx
	return _fn


def step_train_detection(model_name: str = "fasterrcnn_resnet50_fpn", epochs: int = 1, lr: float = 1e-3):
	def _fn(ctx: PipelineContext) -> PipelineContext:
		# TODO: Implement object detection training using torchvision models
		ctx.artifacts["model"] = {
			"task": "detection",
			"arch": model_name,
			"epochs": epochs,
			"lr": lr,
		}
		return ctx
	return _fn


def step_train_segmentation(model_name: str = "deeplabv3_resnet50", epochs: int = 1, lr: float = 1e-3):
	def _fn(ctx: PipelineContext) -> PipelineContext:
		# TODO: Implement segmentation training using torchvision models
		ctx.artifacts["model"] = {
			"task": "segmentation",
			"arch": model_name,
			"epochs": epochs,
			"lr": lr,
		}
		return ctx
	return _fn


def step_evaluate() -> Any:
	def _fn(ctx: PipelineContext) -> PipelineContext:
		# TODO: compute metrics for task
		ctx.metrics.update({"accuracy": 0.0})
		return ctx
	return _fn
