from typing import List
from datetime import datetime
from pydantic import BaseModel, UUID4
from app.schemas.user import UserOut
from app.schemas.product import ProductOut


class OrderItemBase(BaseModel):
    product_id: UUID4
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: UUID4
    product: ProductOut

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    status: str = 'Pending'
    total_price: float


class OrderCreate(OrderBase):
    user_id: UUID4
    items: List[OrderItemCreate]


class OrderOut(OrderBase):
    id: UUID4
    user: UserOut
    items: List[OrderItemOut]
    created_at: datetime

    class Config:
        orm_mode = True
