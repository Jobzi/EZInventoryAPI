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


class UserUpdate(BaseModel):
    uuid: UUID
    phone: str


class UserRoleByTenant(BaseModel):
    uuid: UUID
    user_uuid: UUID
    tenant_uuid: UUID
    role_uuid: UUID

    class Config:
        orm_mode = True


class UserRoleByTenantCreate(BaseModel):
    user_uuid: UUID
    tenant_uuid: UUID
    roles: List[UUID]
