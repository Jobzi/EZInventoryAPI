from typing import Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel

from .base import BaseTable


class Product(BaseTable):
    uuid: UUID
    name: str
    description: str
    public_unit_price: int
    provicer_unit_price: int
    reorder_level: int
    reorder_ammount: int
    picture_path: AnyUrl
    meta: Optional[dict]

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    tenant_uuid: UUID
    category_uuid: UUID
    user_uuid: UUID
    name: str
    description: str
    public_unit_price: int
    provicer_unit_price: int
    reorder_level: int
    reorder_ammount: int
    picture_path: Optional[AnyUrl]
    meta: Optional[dict]
    initial_stock: int


class ProductUpdate(BaseModel):
    tenant_uuid: Optional[UUID]
    category_uuid: Optional[UUID]
    name: Optional[str]
    description: Optional[str]
    public_unit_price: Optional[int]
    provicer_unit_price: Optional[int]
    reorder_level: Optional[int]
    reorder_ammount: Optional[int]
    picture_path: Optional[AnyUrl]
    meta: Optional[dict]
