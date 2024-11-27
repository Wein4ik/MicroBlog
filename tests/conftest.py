import pytest
from fastapi.testclient import TestClient
from api.main_api import app
from datetime import datetime


# Фикстура для тестового клиента
@pytest.fixture()
def test_client():
    """
    Создает и возвращает TestClient для использования в тестах.
    """
    client = TestClient(app)
    yield client


@pytest.fixture()
def fixed_date():
    """
    Returns a fixed datetime for testing purposes
    """
    return datetime(2024, 11, 19, 17, 8, 9, 565605)
