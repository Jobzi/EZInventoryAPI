
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


def test_user_basic_update(client, create_user):
    new_phone = '0123456789'
    user = create_user.json()
    response = client.patch(
        '/user',
        json={
            'uuid': user['uuid'],
            'phone': new_phone
        }
    )
    updated_user = response.json()
    assert response.status_code == 200
    assert updated_user['phone'] == new_phone


def test_delete_user(client, create_user):
    user = create_user.json()
    uri = f"/user/{user['uuid']}"
    response = client.delete(uri)
    check_deleted_user = client.get(uri)
    assert response.status_code == 200
    assert response.json()['uuid'] == user['uuid']
    assert not check_deleted_user.json()


def test_get_tenants_related_to_user(client, create_user):
    user = create_user.json()
    response = client.get(f"/user/{user['uuid']}/tenants")
    tenants = response.json()
    assert response.status_code == 200
    assert isinstance(tenants, list)
    assert len(tenants) > 0


def test_add_tenant_role_to_user(client, create_user, create_role):
    user = create_user.json()
    user_uuid = user['uuid']
    role_uuid = create_role.json()['uuid']
    tenant_response = client.get(f"/user/{user_uuid}/tenants")
    tenant_uuid = tenant_response.json().pop()['uuid']
    response = client.post('/user/role',
                           json={
                               'user_uuid': user_uuid,
                               'tenant_uuid': tenant_uuid,
                               'roles': [role_uuid, ]
                           })

    result = response.json()
    assert response.status_code == 200
    assert isinstance(result, list)
    assert len(result) == 1
    new_user_role_by_tenant = result.pop()
    assert new_user_role_by_tenant['tenant_uuid'] == tenant_uuid
    assert new_user_role_by_tenant['role_uuid'] == role_uuid
    assert new_user_role_by_tenant['user_uuid'] == user_uuid
