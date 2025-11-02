from typing import Callable, Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class StepStatus(str, Enum):
	PENDING = "PENDING"
	RUNNING = "RUNNING"
	SUCCESS = "SUCCESS"
	FAILED = "FAILED"


@dataclass
class PipelineContext:
	data: Dict[str, Any] = field(default_factory=dict)
	artifacts: Dict[str, Any] = field(default_factory=dict)
	metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineStep:
	name: str
	func: Callable[[PipelineContext], PipelineContext]
	status: StepStatus = StepStatus.PENDING
	started_at: Optional[datetime] = None
	finished_at: Optional[datetime] = None
	message: Optional[str] = None

	def run(self, ctx: PipelineContext) -> PipelineContext:
		self.status = StepStatus.RUNNING
		self.started_at = datetime.utcnow()
		try:
			result = self.func(ctx)
			self.status = StepStatus.SUCCESS
			self.finished_at = datetime.utcnow()
			return result
		except Exception as exc:  # noqa: BLE001
			self.status = StepStatus.FAILED
			self.finished_at = datetime.utcnow()
			self.message = str(exc)
			raise


@dataclass
class Pipeline:
	name: str
	steps: List[PipelineStep]
	status: StepStatus = StepStatus.PENDING
	started_at: Optional[datetime] = None
	finished_at: Optional[datetime] = None

	def run(self, initial: Optional[PipelineContext] = None) -> PipelineContext:
		self.status = StepStatus.RUNNING
		self.started_at = datetime.utcnow()
		ctx = initial or PipelineContext()
		for step in self.steps:
			ctx = step.run(ctx)
		self.status = StepStatus.SUCCESS
		self.finished_at = datetime.utcnow()
		return ctx

