import asyncio

import pytest
from app.db.postgre_connector import PostgreSqlConnector
from app.db.sqlite_connector import SqLiteConnector
from app.main import app
from fastapi.testclient import TestClient

# Import fixtures to make them avilable for all tests
from app.tests.fixtures.user import *

app.dependency_overrides[PostgreSqlConnector.get_db] = SqLiteConnector.get_db


@pytest.fixture
def client():
    yield TestClient(app)


def pytest_configure(config):
    asyncio.get_event_loop().run_until_complete(SqLiteConnector.create_db('app.models', 'ezinventory_models'))


def pytest_sessionfinish(session, exitstatus):
    pass
