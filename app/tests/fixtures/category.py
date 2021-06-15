import asyncio
from typing import Callable

import pytest
from app.models.ezinventory_models import Category

from ..test_utils import functions


@pytest.fixture
def category():
    return {
        'name': functions.get_random_string(),
        'description': functions.get_random_string()
    }

#temporary until category endpoint is ready
@pytest.fixture
def create_category(db_session: Callable, category: dict):
    async def insert_into_db(_category):
        async for db in db_session():
            db_category = Category(**_category)
            db.add(db_category)
            await db.commit()
            await db.refresh(db_category)
            return db_category
    db_category = asyncio.get_event_loop().run_until_complete(insert_into_db(category))
    return db_category
