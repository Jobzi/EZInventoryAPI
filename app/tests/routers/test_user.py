
def test_create_user(create_user):
    user = create_user.json()
    assert user
    assert 'password' not in user
    assert create_user.status_code == 200


def test_get_user_by_uuid(client, create_user):
    user = create_user.json()
    response = client.get(
        f"/user/{user['uuid']}"
    )
    response_user = response.json()
    assert response.status_code == 200
    assert 'password' not in response_user
    for key in user:
        assert response_user[key] == user[key]
