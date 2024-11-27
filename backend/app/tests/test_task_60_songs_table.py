import pytest
from models.song import Song, SongInput
from crud.song import get_song_by_id, get_songs_by_artist_id, get_artist_by_song_id, get_all_songs, create_song, update_song, delete_song
from tests.utils import create_random_artist, create_random_song, get_session

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
        db.rollback()
        db.close()

# Test 1: Get song by ID
def test_get_song_by_id(db_session):

    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    retrieved_song = get_song_by_id(db_session, song.song_id)
    assert retrieved_song.title is not None
    assert retrieved_song.title == song.title
    assert retrieved_song.album == song.album
    assert retrieved_song.genre == song.genre
    assert retrieved_song.release_date == song.release_date
    assert retrieved_song.artist_id == song.artist_id

    # Delete the song
    db_session.delete(retrieved_song)
    db_session.commit()

    # Check if the song is deleted
    assert db_session.query(Song).filter(Song.song_id == song.song_id).first() is None

    # Delete the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 2: Get songs by artist_id
def test_get_songs_by_artist_id(db_session):
    artist = create_random_artist(db_session)
    song1 = create_random_song(db_session, artist.user.username)
    song2 = create_random_song(db_session, artist.user.username)

    retrieved_songs = get_songs_by_artist_id(db_session, artist.artist_id)
    assert len(retrieved_songs) == 2
    assert retrieved_songs[0].title == song1.title
    assert retrieved_songs[1].title == song2.title

    # Delete the songs
    db_session.delete(retrieved_songs[0])
    db_session.delete(retrieved_songs[1])
    db_session.commit()

    # Check if the songs are deleted
    assert db_session.query(Song).filter(Song.song_id == song1.song_id).first() is None
    assert db_session.query(Song).filter(Song.song_id == song2.song_id).first() is None

    # Delete the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 3: Get artist by song_id
def test_get_artist_by_song_id(db_session):
    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    retrieved_artist = get_artist_by_song_id(db_session, song.song_id)
    assert retrieved_artist.artist_id == artist.artist_id

    # Delete the song
    db_session.delete(song)
    db_session.commit()

    # Check if the song is deleted
    assert db_session.query(Song).filter(Song.song_id == song.song_id).first() is None

    # Delete the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 4: Get all songs
def test_get_all_songs(db_session):
    artist = create_random_artist(db_session)
    song1 = create_random_song(db_session, artist.user.username)
    song2 = create_random_song(db_session, artist.user.username)

    retrieved_songs = get_all_songs(db_session)
    assert len(retrieved_songs) == 2
    assert retrieved_songs[0].title == song1.title
    assert retrieved_songs[1].title == song2.title

    # Delete the songs
    db_session.delete(retrieved_songs[0])
    db_session.delete(retrieved_songs[1])
    db_session.commit()

    # Check if the songs are deleted
    assert db_session.query(Song).filter(Song.song_id == song1.song_id).first() is None
    assert db_session.query(Song).filter(Song.song_id == song2.song_id).first() is None

    # Delete the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 5: Create a song
def test_create_song(db_session):
    artist = create_random_artist(db_session)
    song_data = {
        "title": "Title",
        "album": "Album",
        "genre": "Genre",
        "release_date": "2024-11-26",
        "artist_name": artist.user.username
    }

    new_song = create_song(db_session, SongInput(**song_data))
    assert new_song.title == "Title"
    assert new_song.album == "Album"
    assert new_song.genre == "Genre"
    assert new_song.release_date == "2024-11-26"
    assert new_song.artist_id == artist.artist_id

    # Delete the song
    db_session.delete(new_song)
    db_session.commit()

    # Check if the song is deleted
    assert db_session.query(Song).filter(Song.song_id == new_song.song_id).first() is None

    # Delete the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 6: Update a song
def test_update_song(db_session):
    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    song_data = {
        "title": "Updated Title",
        "album": "Updated Album",
        "genre": "Updated Genre",
        "release_date": "2024-11-26",
        "artist_name": artist.user.username
    }

    updated_song = update_song(db_session, song.song_id, SongInput(**song_data))
    assert updated_song.title == "Updated Title"
    assert updated_song.album == "Updated Album"
    assert updated_song.genre == "Updated Genre"
    assert updated_song.release_date == "2024-11-26"
    assert updated_song.artist_id == artist.artist_id

    # Delete the song
    db_session.delete(updated_song)
    db_session.commit()

    # Check if the song is deleted
    assert db_session.query(Song).filter(Song.song_id == song.song_id).first() is None

    # Delete the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 7: Delete a song
def test_delete_song(db_session):
    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    delete_song(db_session, song.song_id)
    assert db_session.query(Song).filter(Song.song_id == song.song_id).first() is None

    # Delete the artist
    db_session.delete(artist.user)
    db_session.commit()