from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.models.dataset import Dataset, ImageAsset, Annotation
from app.schemas.dataset import (
	DatasetCreate, DatasetOut,
	ImageCreate, ImageOut,
	AnnotationCreate, AnnotationOut,
)

router = APIRouter()

@router.post("/datasets", response_model=DatasetOut)
def create_dataset(body: DatasetCreate, db: Session = Depends(get_db)):
	ds = Dataset(name=body.name, description=body.description)
	db.add(ds)
	db.commit()
	db.refresh(ds)
	return ds

@router.get("/datasets", response_model=List[DatasetOut])
def list_datasets(db: Session = Depends(get_db)):
	return db.query(Dataset).all()

@router.post("/images", response_model=ImageOut)
def add_image(body: ImageCreate, db: Session = Depends(get_db)):
	ds = db.query(Dataset).filter(Dataset.id == body.dataset_id).first()
	if not ds:
		raise HTTPException(status_code=404, detail="Dataset not found")
	img = ImageAsset(
		dataset_id=body.dataset_id,
		path=body.path,
		width=body.width,
		height=body.height,
	)
	db.add(img)
	db.commit()
	db.refresh(img)
	return img

@router.get("/datasets/{dataset_id}/images", response_model=List[ImageOut])
def list_images(dataset_id: int, db: Session = Depends(get_db)):
	return db.query(ImageAsset).filter(ImageAsset.dataset_id == dataset_id).all()

@router.post("/annotations", response_model=AnnotationOut)
def add_annotation(body: AnnotationCreate, db: Session = Depends(get_db)):
	img = db.query(ImageAsset).filter(ImageAsset.id == body.image_id).first()
	if not img:
		raise HTTPException(status_code=404, detail="Image not found")
	ann = Annotation(
		image_id=body.image_id,
		label=body.label,
		x=body.x,
		y=body.y,
		w=body.w,
		h=body.h,
	)
	db.add(ann)
	db.commit()
	db.refresh(ann)
	return ann

@router.get("/datasets/{dataset_id}/export/coco")
def export_coco(dataset_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
	# TODO: Build proper COCO dict from images and annotations
	return {"info": {}, "images": [], "annotations": [], "categories": []}

@router.get("/datasets/{dataset_id}/export/yolo")
def export_yolo(dataset_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
	# TODO: Return YOLO txt content mapping per image
	return {"format": "yolo", "files": []}

