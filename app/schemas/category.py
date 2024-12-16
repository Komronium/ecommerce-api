from uuid import UUID
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: UUID

    class Config:
        orm_mode = True
