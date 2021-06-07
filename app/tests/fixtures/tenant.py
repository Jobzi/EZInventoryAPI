
import asyncio
from typing import Callable

import pytest
from app.models.ezinventory_models import Tenant

from ..test_utils import functions


@pytest.fixture
def tenant():
    return {
        'name': functions.get_random_string(),
        'main_address': {
            'main_street': 'test street'
        },
        'phone': functions.get_random_phone(),
        'email': functions.get_random_email(),
        'description': 'test tenant'
    }


@pytest.fixture
def create_tenant(db_session: Callable, tenant: dict):
    async def insert_into_db(_tenant):
        async for db in db_session():
            db_tenant = Tenant(**_tenant)
            db.add(db_tenant)
            await db.commit()
            await db.refresh(db_tenant)
            return db_tenant
    db_tenant = asyncio.get_event_loop().run_until_complete(insert_into_db(tenant))
    return db_tenant
