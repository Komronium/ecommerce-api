from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductOut
from app.api.deps import get_db_dependency

router = APIRouter()


@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db_dependency)):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        is_available=product.is_available,
        category_id=product.category_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db_dependency)):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: UUID, db: Session = Depends(get_db_dependency)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: UUID, updated_data: ProductCreate, db: Session = Depends(get_db_dependency)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    category = db.query(Category).filter(Category.id == updated_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    product.name = updated_data.name
    product.description = updated_data.description
    product.price = updated_data.price
    product.stock = updated_data.stock
    product.is_available = updated_data.is_available
    product.category_id = updated_data.category_id
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: UUID, db: Session = Depends(get_db_dependency)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
