from uuid import UUID

from pydantic import BaseModel

from .base import BaseTable


class Category(BaseTable):
    uuid: UUID
    name: str
    description: str

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str
    description: str
