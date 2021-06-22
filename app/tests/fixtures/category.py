import pytest
from fastapi.testclient import TestClient

from ..test_utils import functions


@pytest.fixture
def category():
    return {
        'name': functions.get_random_string(),
        'description': functions.get_random_string()
    }


@pytest.fixture
def create_category(client: 'TestClient', category: dict):
    response = client.post(
        '/category',
        json=category
    )
    return response
