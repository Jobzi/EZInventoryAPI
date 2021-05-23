from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Role(BaseModel):
    uuid: UUID
    name: str
    permissions: dict

    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    name: str
    permissions: dict
