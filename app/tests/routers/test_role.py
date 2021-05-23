
def test_create_role(create_role):
    role = create_role.json()
    assert role
    assert create_role.status_code == 200


def test_get_role_by_uuid(client, create_role):
    role = create_role.json()
    response = client.get(
        f"/role/{role['uuid']}"
    )
    response_role = response.json()
    assert response.status_code == 200
    for key in role:
        assert response_role[key] == role[key]
