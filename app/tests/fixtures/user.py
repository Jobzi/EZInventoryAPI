import pytest
from fastapi.testclient import TestClient

from ..test_utils import functions


@pytest.fixture
def user():
    return {
        'username': functions.get_random_string(),
        'password': functions.get_random_string(),
        'email': functions.get_random_email(),
        'phone': functions.get_random_phone()
    }


@pytest.fixture
def user_with_tenant_and_roles():
    return {
        'username': functions.get_random_string(),
        'password': functions.get_random_string(),
        'email': functions.get_random_email(),
        'phone': functions.get_random_phone(),
        'tenant_uuid': '',
        'roles': []
    }


@pytest.fixture
def create_user(client: 'TestClient', user: dict):
    response = client.post(
        '/user',
        json=user
    )
    return response
