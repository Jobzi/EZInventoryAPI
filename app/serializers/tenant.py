from uuid import UUID

from pydantic import BaseModel, EmailStr

from .base import Address, BaseTable


class Tenant(BaseTable):
    uuid: UUID
    name: str
    main_address: Address
    phone: str
    email: EmailStr
    description: str


class TenantCreate(BaseModel):
    name: str
    main_address: Address
    phone: str
    email: str
    description: str
