from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.product import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.api.deps import get_db_dependency

router = APIRouter()


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db_dependency)):
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists.")

    new_category = Category(name=category.name, description=category.description)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db_dependency)):
    return db.query(Category).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: UUID, db: Session = Depends(get_db_dependency)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: UUID, updated_data: CategoryCreate, db: Session = Depends(get_db_dependency)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    category.name = updated_data.name
    category.description = updated_data.description
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(category_id: UUID, db: Session = Depends(get_db_dependency)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
