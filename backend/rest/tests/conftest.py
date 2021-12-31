import pytest
from fastapi.testclient import TestClient

from backend.rest.main import app


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    client = TestClient(app)
    yield client
