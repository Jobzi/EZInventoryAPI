
def test_create_category(create_category):
    category = create_category.json()
    assert category
    assert create_category.status_code == 200


def test_get_category_by_uuid(client, create_category):
    category = create_category.json()
    response = client.get(
        f"/category/{category['uuid']}"
    )
    response_category = response.json()
    assert response.status_code == 200
    for key in category:
        assert response_category[key] == category[key]
