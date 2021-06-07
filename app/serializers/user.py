from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr

from .base import BaseTable


class User(BaseTable):
    uuid: UUID
    username: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    tenant_uuid: UUID
    roles: List[UUID]
    username: str
    password: str
    email: EmailStr
    phone: str
