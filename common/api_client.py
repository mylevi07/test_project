# common/api_client.py
import requests
import yaml
from pathlib import Path

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}/{endpoint.lstrip('/')}", **kwargs)

    def post(self, endpoint, **kwargs):
        return self.session.post(f"{self.base_url}/{endpoint.lstrip('/')}", **kwargs)

    def put(self, endpoint, **kwargs):
        return self.session.put(f"{self.base_url}/{endpoint.lstrip('/')}", **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.session.delete(f"{self.base_url}/{endpoint.lstrip('/')}", **kwargs)


def load_config():
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)