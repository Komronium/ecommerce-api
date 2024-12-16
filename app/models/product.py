from uuid import uuid4
from sqlalchemy import Column, Uuid, String, Float, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Category(Base):
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(Uuid(as_uuid=True), ForeignKey('category.id'))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)

    category = relationship("Category", back_populates="products")

