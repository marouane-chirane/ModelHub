from pydantic import BaseModel
from typing import Optional, List

class DatasetCreate(BaseModel):
	name: str
	description: Optional[str] = None

class DatasetOut(BaseModel):
	id: int
	name: str
	description: Optional[str] = None
	class Config:
		from_attributes = True

class ImageCreate(BaseModel):
	dataset_id: int
	path: str
	width: Optional[int] = None
	height: Optional[int] = None

class ImageOut(BaseModel):
	id: int
	dataset_id: int
	path: str
	width: Optional[int] = None
	height: Optional[int] = None
	class Config:
		from_attributes = True

class AnnotationCreate(BaseModel):
	image_id: int
	label: str
	x: float
	y: float
	w: float
	h: float

class AnnotationOut(BaseModel):
	id: int
	image_id: int
	label: str
	x: float
	y: float
	w: float
	h: float
	class Config:
		from_attributes = True

