import pytest
from fastapi.testclient import TestClient
from app.utils.constants import DniTypes

from ..test_utils import functions, mocks


@pytest.fixture
def customer():
    return {
        'name': functions.get_random_string(),
        'dni': functions.get_random_sequence(10),
        'dni_type': functions.get_random_choice([_type.value for _type in DniTypes]),
        'main_address': mocks.mock_address(),
        'phone': functions.get_random_phone(),
        'email': functions.get_random_email(),
        'description': 'test customer',
        'meta': {
            'meta_key': 'meta_example'
        }
    }


@pytest.fixture
def create_customer(client: 'TestClient', customer: dict):
    response = client.post(
        '/customer',
        json=customer
    )
    return response
