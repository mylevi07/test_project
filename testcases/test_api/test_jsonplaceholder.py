# testcases/test_api/test_jsonplaceholder.py
import pytest
from common.api_client import APIClient, load_config

config = load_config()
json_placeholder_url = config["json_placeholder"]["base_url"]
client = APIClient(json_placeholder_url)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]