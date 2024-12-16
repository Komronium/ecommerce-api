from uuid import UUID
from fastapi import  HTTPException
from sqlalchemy.orm import Session

from app.models.product import Category



def get_category_by_id(category_id: UUID, db: Session) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    return category
