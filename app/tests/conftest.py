import asyncio

import pytest
from app.db.postgre_connector import PostgreSqlConnector
from app.db.sqlite_connector import SqLiteConnector
from app.main import app
from app.security import AuthFunctions, auth_user, mock_auth_user

# Import fixtures to make them avilable for all tests
from app.tests.fixtures.role import *
from app.tests.fixtures.tenant import *
from app.tests.fixtures.user import *

from fastapi.testclient import TestClient

app.dependency_overrides[PostgreSqlConnector.get_db] = SqLiteConnector.get_db
app.dependency_overrides[auth_user] = mock_auth_user


@pytest.fixture
def client():
    yield TestClient(app)


def mock_check_permission_mapping_by_uuid(*args, **kwargs):
    pass


def mock_check_own_permission_by_uuid(*args, **kwargs):
    pass


@pytest.fixture
def db_session():
    return SqLiteConnector.get_db


@pytest.fixture(autouse=True)
def patch_auth_functions(monkeypatch):

    monkeypatch.setattr(
        AuthFunctions,
        'check_permission_mapping_by_uuid',
        mock_check_permission_mapping_by_uuid)

    monkeypatch.setattr(
        AuthFunctions,
        'check_own_permission_by_uuid',
        mock_check_own_permission_by_uuid)


def pytest_configure(config):
    asyncio.get_event_loop().run_until_complete(SqLiteConnector.create_db('app.models', 'ezinventory_models'))


def pytest_sessionfinish(session, exitstatus):
    pass
