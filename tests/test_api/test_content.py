from unittest.mock import patch

from api.schemas.schemas import GetContentSchema
from core.exceptions import ContentNotFoundException
from repository.models import ContentType


def test_get_content_success(test_client, fixed_date):
    """
    Test successful content get via the API.
    Ensures status code 200, correct response, and repository/transaction calls.
    """

    # Arrange
    with patch("repository.sqlalchemy_repository.SQLAlchemyContentRepository.get_content") as mock_get:
        mock_get.return_value = GetContentSchema(
            id=1,
            created_at=fixed_date,
            content='content',
            content_type=ContentType.POST,
            user_id=1,
            parent_id=None
        )

        # Act
        response = test_client.get("/content/1")

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "created_at": fixed_date.isoformat(),
            "content": 'content',
            "content_type": ContentType.POST.value,
            "user_id": 1,
            "parent_id": None
        }

        mock_get.assert_called()


def test_get_content_returns_404_when_not_found(test_client):
    """
    Test API behavior when attempting to retrieve a non-existent content.
    Ensures:
    - Status code 404.
    - Correct error message in the 'detail' field.
    """

    # Arrange
    content_id = 1
    with patch("repository.sqlalchemy_repository.SQLAlchemyContentRepository.get_content") as mock_get:
        mock_get.side_effect = ContentNotFoundException()

        # Act
        response = test_client.get(f"/content/{content_id}")

        # Assert
        assert response.status_code == 404
        assert 'detail' in response.json()
        assert response.json().get('detail') == f"Content with ID {content_id} not found"

        mock_get.assert_called_once_with(content_id)


def test_get_content_invalid_id_type(test_client):
    """
   Test API behavior when an invalid content ID is provided.

   This test verifies:
   - A non-integer value in the path parameter (e.g., "invalid_id") returns status code 422.
   - A zero value (0) in the path parameter returns status code 422.
   - A negative value (-1) in the path parameter returns status code 422.
   """
    response = test_client.get("/content/invalid_id")
    assert response.status_code == 422

    response = test_client.get("/content/0")
    assert response.status_code == 422

    response = test_client.get("/content/-1")
    assert response.status_code == 422
