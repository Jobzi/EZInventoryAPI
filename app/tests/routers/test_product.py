import pytest


def test_create_product(create_product):
    product = create_product.json()
    assert product
    assert create_product.status_code == 200


def test_get_product_by_uuid(client, create_product):
    product = create_product.json()
    response = client.get(
        f"/product/{product['uuid']}"
    )
    response_product = response.json()
    assert response.status_code == 200
    for key in product:
        assert response_product[key] == product[key]


@pytest.mark.parametrize('update_values', [
    {'name': 'test update'},
    {'public_unit_price': 99},
    {'provicer_unit_price': 300,
     'reorder_level': 9,
     'reorder_ammount': 90,
     'picture_path': 'http://www.exampletest.com',
     'meta': {'new_meta': 'new_meta'}},
])
def test_product_basic_update(client, create_product, update_values):
    product = create_product.json()
    response = client.put(
        f"/product/{product['uuid']}",
        json={
            **update_values
        }
    )
    updated_product = response.json()
    assert response.status_code == 200
    for key, value in update_values.items():
        assert key in updated_product
        assert updated_product[key] == value


def test_delete_product(client, create_product):
    product = create_product.json()
    uri = f"/product/{product['uuid']}"
    response = client.delete(uri)
    check_deleted_product = client.get(uri)
    assert response.status_code == 200
    assert response.json()['uuid'] == product['uuid']
    assert not check_deleted_product.json()
