import pytest


@pytest.mark.order(1)
def test_follow_user(api_client_user1, api_client_user2):
    user = api_client_user2.get("/user/user2/").json()

    response = api_client_user1.post(F"/user/follow/{user['id']}")
    assert response.status_code == 201

@pytest.mark.order(2)
def test_not_allow_follow_same_user(api_client_user1):
    user = api_client_user1.get("/user/user1/").json()

    response = api_client_user1.post(F"/user/follow/{user['id']}")
    assert response.status_code == 400

@pytest.mark.order(3)
def test_like_a_post(api_client_user1, api_client_user2):
    response = api_client_user1.post(
        "/post/",
        json={
            "text": f"hello follower",
        },
    )

    assert response.status_code == 201
    result = response.json()

    response2 = api_client_user2.post(F"/post/{result['id']}/like/")
    assert response2.status_code == 201

def test_get_posts_with_like(api_client):
    user = api_client.get("/user/user2/").json()
    response = api_client.get(F"/post/likes/{user['id']}")

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
