# testcases/test_api/test_jsonplaceholder.py
import pytest
from common.api_client import APIClient, load_config

config = load_config()
json_placeholder_url = config["json_placeholder"]["base_url"]
client = APIClient(json_placeholder_url)


def test_get_all_users():
    """TC01: 获取所有用户"""
    response = client.get("/users")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]


def test_get_single_user():
    """TC02: 获取单个用户"""
    user_id = 1
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    user = response.json()
    assert user["id"] == user_id
    assert "name" in user
    assert "email" in user


def test_create_post():
    """TC03: 创建新帖子"""
    payload = {
        "title": "test title",
        "body": "test body",
        "userId": 1
    }
    response = client.post("/posts", json=payload)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data


def test_update_post():
    """TC04: 更新帖子"""
    post_id = 1
    payload = {
        "id": post_id,
        "title": "updated title",
        "body": "updated body",
        "userId": 1
    }
    response = client.put(f"/posts/{post_id}", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["title"] == "updated title"


def test_delete_post():
    """TC05: 删除帖子"""
    post_id = 1
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"


def test_get_nonexistent_user():
    """反向：获取不存在的用户，应返回 404"""
    response = client.get("/users/999999999")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


def test_create_post_response_schema():
    """可靠性：创建帖子响应包含必要字段，且 title 与入参一致"""
    payload = {"title": "schema check", "body": "body", "userId": 1}
    response = client.post("/posts", json=payload)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    data = response.json()
    assert {"title", "id", "userId"} <= set(data.keys())
    assert data["title"] == payload["title"]