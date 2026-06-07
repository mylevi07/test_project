# testcases/conftest.py
import pytest
import logging
from common.logger import setup_logger

logger = setup_logger("test")

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="test",
        help="测试环境: test 或 staging"
    )

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(autouse=True)
def log_test(request):
    logger.info(f"========== START: {request.node.name} ==========")
    yield
    logger.info(f"========== END: {request.node.name} ==========")