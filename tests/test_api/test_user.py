from datetime import datetime
from unittest.mock import patch

from api.schemas.schemas import GetUserSchema
from repository.entities.entities import UserEntity


def test_add_user_success(test_client):
    # Arrange
    dt = datetime(2024, 11, 19, 17, 8, 9, 565605)
    with patch("repository.sqlalchemy_repository.SQLAlchemyUserRepository.add") as mock_add:
        mock_add.return_value = GetUserSchema(
            id=1,
            username='testuser',
            created_at=dt,
        )

        # Act
        response = test_client.post("/user/create", json={"username": "testuser"})

        # Assert
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "username": "testuser",
            "created_at": dt.isoformat()
        }
        mock_add.assert_called_once_with("testuser")