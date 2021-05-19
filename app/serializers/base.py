from datetime import datetime
from typing import Optional
from app.utils.constants import StatusConstants

from pydantic import BaseModel


class BaseTable(BaseModel):
    created_on: datetime
    updated_on: datetime
    status: StatusConstants
    activated_on: Optional[datetime]
    deleted_on: Optional[datetime]
    reactivated_on: Optional[datetime]
