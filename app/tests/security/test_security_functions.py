import asyncio
from datetime import timedelta
from uuid import uuid4

import pytest
from app.security.exeptions import (InvalidCredentialsError,
                                    NotEnoughPermissionsError)
from app.security.functions import AuthFunctions, JWTFunctions
from app.tests.test_utils import functions
from fastapi.security import SecurityScopes
from jose import JWTError


def mock_data_for_token():
    return {'sub': 'username'}


def mock_access_token():
    return JWTFunctions.create_access_token(mock_data_for_token())


def mock_invalid_user_token():
    return JWTFunctions.create_access_token({'sub': 'unknownuser'})


def mock_not_enough_permissions_user_token():
    return JWTFunctions.create_access_token({'sub': 'notenoughuser'})


def mock_no_sub_token():
    return JWTFunctions.create_access_token({'sub1': 'invalid'})


def mock_expired_token():
    return JWTFunctions.create_access_token(mock_data_for_token(), timedelta(-1))


def mock_permissions():
    return ('scope1', 'scope2', 'scope3')


@pytest.fixture
def mock_db():
    permission_choices = mock_permissions()
    return {
        'username': {
            'permissions': {
                'tenant1': permission_choices,
                'tenant2': permission_choices[:2],
                'tenant3': [],
                'tenant4': permission_choices[:1]
            },
            'user_info': {}
        },
        'notenoughuser': {
            'permissions': {},
            'user_info': {}
        }
    }


def mock_check_user_permissions_wrapper(db, permissions, token):

    async def mock_get_user(_db, username):
        return _db.get(username)

    return asyncio.get_event_loop().run_until_complete(AuthFunctions.check_user_permissions(
        db, mock_get_user, SecurityScopes(permissions), token
    ))


@pytest.mark.parametrize(
    ('data', 'expire_delta'),
    [(mock_data_for_token(), None),
     (mock_data_for_token(), timedelta(1)),
     ])
def test_create_access_token(data, expire_delta):
    token = JWTFunctions.create_access_token(data, expire_delta)
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_token():
    decoded_token = JWTFunctions.decode_token(mock_access_token())
    assert isinstance(decoded_token, dict)
    assert 'sub' in decoded_token
    assert 'exp' in decoded_token


def test_decode_broken_token():
    with pytest.raises(JWTError):
        JWTFunctions.decode_token(functions.get_random_string())


@pytest.mark.parametrize(('permissions', 'token', 'result'), [
    ([], functions.get_random_string(), InvalidCredentialsError),
    ([], mock_no_sub_token(), InvalidCredentialsError),
    ([], mock_expired_token(), InvalidCredentialsError),
    ([], mock_invalid_user_token(), InvalidCredentialsError),
    ([], mock_not_enough_permissions_user_token(), NotEnoughPermissionsError),
    (['scope4'], mock_access_token(), NotEnoughPermissionsError)
])
def test_check_invalid_user_permissions(permissions, token, result, mock_db):
    with pytest.raises(result):
        mock_check_user_permissions_wrapper(mock_db, permissions, token)


def test_check_permission_mapping_by_uuid(monkeypatch):
    monkeypatch.undo()
    mock_uuid = str(uuid4())
    AuthFunctions.check_permission_mapping_by_uuid(mock_uuid, {
        'scopes': ['scope1', 'scope2'],
        'permissions_by_tenant': {
            mock_uuid: ['scope1']
        }
    })


@pytest.mark.parametrize('test_scopes', [
    ['scope3'],
    [],
])
def test_check_not_enough_permission_mapping_by_uuid(test_scopes, monkeypatch):
    monkeypatch.undo()
    mock_uuid = str(uuid4())
    with pytest.raises(NotEnoughPermissionsError):
        AuthFunctions.check_permission_mapping_by_uuid(mock_uuid, {
            'scopes': ['scope1, scope2'],
            'permissions_by_tenant': {
                mock_uuid: test_scopes
            }
        })


def test_check_not_own_permission_by_uuid(monkeypatch):
    monkeypatch.undo()
    mock_source_uuid, mock_target_uuid = str(uuid4()), str(uuid4())
    with pytest.raises(NotEnoughPermissionsError):
        AuthFunctions.check_own_permission_by_uuid(mock_source_uuid, mock_target_uuid, ['own'])


def test_check_own_permission_by_uuid(monkeypatch):
    monkeypatch.undo()
    mock_source_uuid = str(uuid4())
    AuthFunctions.check_own_permission_by_uuid(mock_source_uuid, mock_source_uuid, ['own'])
