from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from .base import Address, BaseTable


class Provider(BaseTable):
    uuid: UUID
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: Optional[dict]

    class Config:
        orm_mode = True


class ProviderCreate(BaseModel):
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: Optional[dict]


class ProviderUpdate(BaseModel):
    uuid: UUID
    main_address: Optional[Address]
    phone: Optional[str]
    description: Optional[str]
    meta: Optional[dict]


class ProviderProducts(BaseModel):
    uuid: UUID
    product_uuid: UUID
    provider_uuid: UUID

    class Config:
        orm_mode = True


class ProviderProductsCreate(BaseModel):
    product_uuids: List[UUID]
    provider_uuid: UUID
