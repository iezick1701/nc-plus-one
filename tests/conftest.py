import pytest
from fastapi.testclient import TestClient
from main import app
from db.seed import seed_test


@pytest.fixture
def api_client(test_db):
    return TestClient(app)


@pytest.fixture
def test_db(monkeypatch):
    monkeypatch.setenv("DB_NAME", "nc_plus_one_test")
    seed_test()