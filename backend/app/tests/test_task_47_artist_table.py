import pytest
from tests.utils import create_random_user, get_session
from crud.artist import *
from models.artist import Artist, ArtistInput

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a clean database session for each test.
    Automatically rolls back transactions after each test.
    """
    db = get_session()
    try:
        yield db
    finally:
        # Cleanup: Rollback any changes made during the test
        db.rollback()
        db.close()

# Test: Get artist by user_id
def test_get_artist_by_user_id(db_session):
    user = create_random_user(db_session)
    artist = Artist(user_id=user.id, name="Test Artist", genre="Test Genre", bio="Test Bio")
    db_session.add(artist)
    db_session.commit()
    db_session.refresh(artist)

    retrieved_artist = get_artist_by_user_id(db_session, user.id)
    assert retrieved_artist is not None
    assert retrieved_artist.name == "Test Artist"

# Test: Create an Artist
def test_create_artist(db_session):
    user = create_random_user(db_session)

    artist_input = ArtistInput(
        username=user.username,
        name="Test Artist",
        genre="Pop",
        bio="This is a test bio."
    )

    artist = create_artist(db_session, artist_input)

    db_session.refresh(artist)
    assert artist.name == artist_input.name
    assert artist.genre == artist_input.genre
    assert artist.bio == artist_input.bio
    assert artist.user_id == user.id

# Test: Create artist fails if user is already an artist
def test_create_artist_already_exists(db_session):
    user = create_random_user(db_session)
    artist = Artist(user_id=user.id, name="Existing Artist", genre="Pop", bio="Already famous")
    db_session.add(artist)
    db_session.commit()

    artist_input = ArtistInput(username=user.username, name="Duplicate Artist", genre="Pop", bio="Duplicate bio")
    with pytest.raises(Exception) as exc_info:
        create_artist(db_session, artist_input)
    assert exc_info.value.status_code == 400
    assert "This user is already an artist." in str(exc_info.value.detail)

# Test: Deleting User Cascades to Artist
def test_cascade_delete_user_deletes_artist(db_session):
    user = create_random_user(db_session)

    artist_input = ArtistInput(
        username=user.username,
        name="Cascade Artist",
        genre="Rock",
        bio="This artist will be deleted."
    )
    create_artist(db_session, artist_input)

    assert get_artist_by_user_id(db_session, user.id) is not None

    db_session.delete(user)
    db_session.commit()

    artist_in_db_after = get_artist_by_user_id(db_session, user.id)
    assert artist_in_db_after is None

# Test: Get artist by username
def test_get_artist_by_username(db_session):
    user = create_random_user(db_session)
    artist = Artist(user_id=user.id, name="Username Artist", genre="Rock", bio="Rockstar")
    db_session.add(artist)
    db_session.commit()

    retrieved_artist = get_artist_by_username(db_session, user.username)
    assert retrieved_artist is not None
    assert retrieved_artist.name == "Username Artist"

# Test: Get artist by username fails if not an artist
def test_get_artist_by_username_not_artist(db_session):
    user = create_random_user(db_session)
    with pytest.raises(Exception) as exc_info:
        get_artist_by_username(db_session, user.username)
    assert exc_info.value.status_code == 400
    assert "This user is not an artist." in str(exc_info.value.detail)
