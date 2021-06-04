from typing import Optional
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


class ProviderCreate(BaseModel):
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: Optional[dict]
