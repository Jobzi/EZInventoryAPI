import pytest
from fastapi.testclient import TestClient

from ..test_utils import functions, mocks


@pytest.fixture
def product(create_tenant, create_category, create_user):
    return {
        'tenant_uuid': str(create_tenant.uuid),
        'category_uuid': create_category.json()['uuid'],
        'user_uuid': create_user.json()['uuid'],
        'name': functions.get_random_string(),
        'description': functions.get_random_string(),
        'public_unit_price': 200,
        'provicer_unit_price': 300,
        'reorder_level': 10,
        'reorder_ammount': 20,
        'picture_path': 'http://www.example.com',
        'meta': {},
        'initial_stock': 25
    }


@pytest.fixture
def create_product(client: 'TestClient', product: dict):
    response = client.post(
        '/product',
        json=product
    )
    return response
