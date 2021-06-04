from uuid import UUID

from pydantic import BaseModel

from .base import BaseTable


class Category(BaseTable):
    uuid: UUID
    name: str
    description: str


class CategoryCreate(BaseModel):
    name: str
    description: str
