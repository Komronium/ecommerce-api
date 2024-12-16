from pydantic import BaseModel, UUID4
from app.schemas.category import CategoryResponse


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    is_available: bool = True


class ProductCreate(ProductBase):
    category_id: UUID4


class ProductOut(ProductBase):
    id: UUID4
    category: CategoryResponse

    class Config:
        orm_mode = True
