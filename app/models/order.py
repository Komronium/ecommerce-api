from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Uuid, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class OrderItem(Base):
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4, index=True)
    order_id = Column(Uuid(as_uuid=True), ForeignKey('order.id'))
    product_id = Column(Uuid(as_uuid=True), ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Order(Base):
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey('user.id'))
    total_price = Column(Float, nullable=False)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

