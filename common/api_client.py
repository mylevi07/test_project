# common/api_client.py
import requests
import yaml
from common.logger import setup_logger
from pathlib import Path

logger = setup_logger("api_client")

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def _log_request(self, method, url):
        logger.info(f"{method.upper()} {url}")

    def _log_response(self, response):
        logger.debug(f"Response {response.status_code}: {response.text[:200]}")

    def get(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("GET", url)
        response = self.session.get(url, **kwargs)
        self._log_response(response)
        return response

    def post(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("POST", url)
        response = self.session.post(url, **kwargs)
        self._log_response(response)
        return response

    def put(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("PUT", url)
        response = self.session.put(url, **kwargs)
        self._log_response(response)
        return response

    def delete(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("DELETE", url)
        response = self.session.delete(url, **kwargs)
        self._log_response(response)
        return response


def load_config():
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)