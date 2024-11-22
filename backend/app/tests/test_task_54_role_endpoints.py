import pytest
from fastapi import HTTPException, status
from models.user import RoleEnum
from crud.user import assign_role, get_role
from crud.listener import get_listener_by_user_id
from crud.artist import get_artist_by_user_id
from tests.utils import create_random_user, get_session

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a clean database session for each test.
    Automatically rolls back transactions after each test.
    """
    db = get_session()  # Assume get_session() provides a valid SQLAlchemy session
    try:
        yield db
    finally:
        db.rollback()
        db.close()

### Tests for assign_role ###

def test_assign_role_to_user_without_role(db_session):
    # Arrange
    user = create_random_user(db_session)

    # Act
    assign_role(db_session, user, RoleEnum.listener)

    # Assert
    assert user.role == RoleEnum.listener

    # Listener created
    assert get_listener_by_user_id(db_session, user.id) is not None


def test_assign_role_to_user_with_existing_role(db_session):
    # Arrange
    user = create_random_user(db_session)
    user.role = RoleEnum.artist  # Pre-assign a role
    db_session.commit()

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        assign_role(db_session, user, RoleEnum.listener)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "The user has already a role."

def test_assign_role_creates_listener(db_session):
    # Arrange
    user = create_random_user(db_session)

    # Act
    assign_role(db_session, user, RoleEnum.listener)

    # Assert
    assert user.role == RoleEnum.listener

    # Listener created
    assert get_listener_by_user_id(db_session, user.id) is not None

def test_assign_role_creates_artist(db_session):
    # Arrange
    user = create_random_user(db_session)

    # Act
    assign_role(db_session, user, RoleEnum.artist)

    # Assert
    assert user.role == RoleEnum.artist

    # Artist created
    assert get_artist_by_user_id(db_session, user.id) is not None

### Tests for get_role ###

def test_get_role_of_user_with_role(db_session):
    # Arrange
    user = create_random_user(db_session)
    user.role = RoleEnum.listener
    db_session.commit()

    # Act
    role = get_role(user)

    # Assert
    assert role == RoleEnum.listener

def test_get_role_of_user_with_no_role(db_session):
    # Arrange
    user = create_random_user(db_session)

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_role(user)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "The user has no role."
