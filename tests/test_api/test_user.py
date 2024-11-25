from datetime import datetime
from unittest.mock import patch

from api.schemas.schemas import GetUserSchema
from core.exceptions import UserAlreadyExistsException
from repository.entities.entities import UserEntity


def test_add_user_success(test_client):
    """
    Test successful user creation via the API.
    Ensures status code 201, correct response, and repository/transaction calls.
    """

    # Arrange
    dt = datetime(2024, 11, 19, 17, 8, 9, 565605)
    with patch("repository.sqlalchemy_repository.SQLAlchemyUserRepository.add") as mock_add, \
            patch("repository.unit_of_work.UnitOfWork.commit") as mock_commit:
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
        mock_commit.assert_called_once()


def test_add_existing_user_returns_conflict(test_client):
    """
        Test the behavior of the API when attempting to create a user that already exists.
        Expected:
        - Status code 409 Conflict.
        - Error message in the 'detail' field.
        - Repository's add method called with the correct argument.
        """
    # Arrange
    exception_message = "User with username testuser is already exist"
    with patch("repository.sqlalchemy_repository.SQLAlchemyUserRepository.add") as mock_add:
        mock_add.side_effect = UserAlreadyExistsException(exception_message)

        # Act
        response = test_client.post("/user/create", json={"username": "testuser"})

        # Assert
        assert response.status_code == 409
        assert "detail" in response.json()
        assert response.json().get('detail') == exception_message

        mock_add.assert_called_once_with("testuser")


def test_add_user_invalid_input(test_client):
    """
      Test API behavior when invalid input is provided.
    """

    # Act
    response = test_client.post("/user/create", json={})  # Missing username

    # Assert
    assert response.status_code == 422


def test_add_user_invalid_type(test_client):
    """
    Test API behavior when invalid data type is provided for username.
    """

    # Act
    response = test_client.post("/user/create", json={"username": 1})

    # Assert
    assert response.status_code == 422


def test_add_user_invalid_length_username(test_client):
    """
   Test API behavior when invalid length of username:
   - Empty username
   - Username exceeding maximum length
   """

    response = test_client.post("/user/create", json={"username": ""})
    assert response.status_code == 422

    response = test_client.post("/user/create", json={"username": "a" * 100})
    assert response.status_code == 422
