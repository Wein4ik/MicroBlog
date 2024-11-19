import pytest
from fastapi.testclient import TestClient
from api.main_api import app


# Фикстура для тестового клиента
@pytest.fixture()
def test_client():
    """
    Создает и возвращает TestClient для использования в тестах.
    """
    client = TestClient(app)
    yield client
