import pytest


@pytest.mark.order(1)
def test_follow_user(api_client_user1):
    user = api_client_user1.get("/user/user2/").json()

    response = api_client_user1.post(F"/user/follow/{user['id']}")
    assert response.status_code == 201

def test_not_allow_follow_same_user(api_client_user1):
    user = api_client_user1.get("/user/user1/").json()

    response = api_client_user1.post(F"/user/follow/{user['id']}")
    assert response.status_code == 400