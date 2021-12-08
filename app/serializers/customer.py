from typing import Optional
from uuid import UUID

from app.utils.constants import DniTypes
from pydantic import BaseModel, EmailStr

from .base import Address, BaseTable


class Customer(BaseTable):
    uuid: UUID
    name: str
    dni: str
    dni_type: DniTypes
    main_address: Address
    phone: str
    email: EmailStr
    description: str
    meta: Optional[dict]

    class Config:
        orm_mode = True


class CustomerCreate(BaseModel):
    name: str
    dni: str
    dni_type: DniTypes
    main_address: Address
    phone: str
    email: EmailStr
    description: Optional[str]
    meta: Optional[dict]


class CustomerUpdate(BaseModel):
    uuid: UUID
    name: Optional[str]
    main_address: Optional[Address]
    phone: Optional[str]
    email: Optional[EmailStr]
    description: Optional[str]
    meta: Optional[dict]
