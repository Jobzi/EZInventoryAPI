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


class CustomerCreate(BaseModel):
    name: str
    dni: str
    dni_type: DniTypes
    main_address: Address
    phone: str
    email: EmailStr
    description: Optional[str]
    meta: Optional[dict]
