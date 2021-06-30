import pytest
from fastapi.testclient import TestClient

from ..test_utils import functions, mocks


@pytest.fixture
def provider():
    return {
        'name': functions.get_random_string(),
        'main_address': mocks.mock_address(),
        'phone': functions.get_random_phone(),
        'email': functions.get_random_email(),
        'description': 'test provider',
        'meta': {
            'meta_key': 'meta_example'
        }
    }


@pytest.fixture
def create_provider(client: 'TestClient', provider: dict):
    response = client.post(
        '/provider',
        json=provider
    )
    return response
