from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, validator, EmailStr

from .base import BaseTable


class User(BaseTable):
    uuid: UUID
    username: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    tenant_uuid: Optional[UUID]
    roles: Optional[List[UUID]]
    username: str
    password: str
    email: EmailStr
    phone: str

    @validator('roles', 'tenant_uuid')
    def check_roles_and_tenant(cls, v, values,  **kwargs):
        if 'tenant_uuid' not in values and 'roles' not in values:
            raise ValueError('roles and tenant_uuid should be both included or left empty')
        return v
