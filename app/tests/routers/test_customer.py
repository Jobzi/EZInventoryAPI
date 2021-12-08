import pytest

from app.tests.test_utils.mocks import mock_address


def test_create_customer(create_customer):
    customer = create_customer.json()
    assert customer
    assert create_customer.status_code == 200


def test_get_customer_by_uuid(client, create_customer):
    customer = create_customer.json()
    response = client.get(
        f"/customer/{customer['uuid']}"
    )
    response_customer = response.json()
    assert response.status_code == 200
    assert 'name' in response_customer
    assert 'uuid' in response_customer
    assert 'dni' in response_customer


@pytest.mark.parametrize('update_values', [
    {'phone': '0123456789'},
    {'main_address': mock_address()},
    {'description': 'new description'},
    {'phone': '0123456789',
     'main_address': mock_address(),
     'description': 'new_description',
     'meta': {'new_meta': 'new_meta'}},
])
def test_customer_basic_update(client, create_customer, update_values):
    customer = create_customer.json()
    response = client.patch(
        '/customer',
        json={
            'uuid': customer['uuid'],
            **update_values
        }
    )
    updated_customer = response.json()
    assert response.status_code == 200
    for key, value in update_values.items():
        assert key in updated_customer
        assert updated_customer[key] == value


def get_customers_by_unique_identifier(client, create_customer):
    created_customer = create_customer.json()
    response = client.get(f'/customer/identifier/{created_customer["dni"][:8]}')
    customer_page = response.json()
    assert response.status_code == 200
    assert isinstance(customer_page['items'], list)
    assert len(customer_page['items']) == 1
    assert customer_page['items'][0]['uuid'] == create_customer['uuid']
    assert customer_page['items'][0]['dni'] == create_customer['dni']
    assert customer_page['page'] == 1
    assert customer_page['size'] == 1
    assert customer_page['total'] == 1


def test_delete_customer(client, create_customer):
    customer = create_customer.json()
    uri = f"/customer/{customer['uuid']}"
    response = client.delete(uri)
    check_deleted_customer = client.get(uri)
    assert response.status_code == 200
    assert response.json()['uuid'] == customer['uuid']
    assert not check_deleted_customer.json()
