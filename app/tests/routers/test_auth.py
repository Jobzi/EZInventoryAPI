from fastapi.testclient import TestClient


def test_login_user(client: 'TestClient', user_w_password: dict):
    response = client.post('/auth/login',
                           data={
                               'username': user_w_password['username'],
                               'password': user_w_password['password'],
                           })

    assert response.status_code == 200
    login_result = response.json()
    assert 'access_token' in login_result
    assert len(login_result['access_token']) > 0
    assert 'token_type' in login_result
