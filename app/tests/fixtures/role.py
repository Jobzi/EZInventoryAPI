import pytest
from fastapi.testclient import TestClient

from ..test_utils import functions


@pytest.fixture
def role():
    return {
        'name': functions.get_random_string(),
        'permissions': {}
    }


@pytest.fixture
def create_role(client: 'TestClient', role: dict):
    response = client.post(
        '/role',
        json=role
    )
    return response
