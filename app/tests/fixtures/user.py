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
def user_with_tenant_and_roles(user, create_tenant, create_role):
    return {
        **user,
        'tenant_uuid': str(create_tenant.uuid),
        'roles': [create_role.json().get('uuid')]
    }


@pytest.fixture
def create_user(client: 'TestClient', user_with_tenant_and_roles: dict):
    response = client.post(
        '/user',
        json=user_with_tenant_and_roles
    )
    return response


@pytest.fixture
def user_w_password(client: 'TestClient', user_with_tenant_and_roles: dict):
    response = client.post(
        '/user',
        json=user_with_tenant_and_roles
    )
    return {**response.json(), 'password': user_with_tenant_and_roles['password']}
