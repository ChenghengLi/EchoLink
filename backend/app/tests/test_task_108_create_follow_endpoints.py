from fastapi.testclient import TestClient
from models.user import ListenerArtistLink
from main import app
from core.config import get_db
from tests.utils import create_random_auth_listener, create_random_auth_artist
from crud.listener import get_listener_by_user_id
from crud.artist import get_artist_by_user_id

client = TestClient(app)

# Test for following an artist
def test_follow_artist():
    db = next(get_db())

    # Create a random user
    listener_user = create_random_auth_listener(db)
    artist_user = create_random_auth_artist(db)

    listener = get_listener_by_user_id(db, listener_user.id)
    artist = get_artist_by_user_id(db, artist_user.id)

    response = client.post(
        f"/listeners/follow/{artist.name}",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains the correct data
    assert response.json().get("artist_id") == artist.artist_id
    assert response.json().get("listener_id") == listener.listener_id

    # Assert ListenerArtistLink table contains the listener-artist link
    follow = db.query(ListenerArtistLink).filter(
        ListenerArtistLink.listener_id == listener.listener_id,
        ListenerArtistLink.artist_id == artist.artist_id
    ).first()
    assert follow is not None

    # Clean up the database
    db.delete(listener)
    db.delete(artist)
    db.commit()

#Test for following an artist being an artist
def test_follow_artist_as_artist():
    db = next(get_db())

    # Create two random artists
    artist1_user = create_random_auth_artist(db)
    artist2_user = create_random_auth_artist(db)

    artist1 = get_artist_by_user_id(db, artist1_user.id)
    artist2 = get_artist_by_user_id(db, artist2_user.id)

    # Call the /follow/{artist_name} endpoint
    response = client.post(
        f"/listeners/follow/{artist2.name}",
        headers={"Authorization": f"Bearer {artist1_user.token}"}
    )

    # Assert the response status code
    assert response.status_code == 400
    assert response.json() == {"detail": "You must be a listener to follow an artist."}

    # Clean up the database
    db.delete(artist1)
    db.delete(artist2)
    db.commit()

# Test for following an artist that the listener is already following
def test_follow_artist_already_following():
    db = next(get_db())

    # Create a random listener and artist
    listener_user = create_random_auth_listener(db)
    artist_user = create_random_auth_artist(db)

    listener = get_listener_by_user_id(db, listener_user.id)
    artist = get_artist_by_user_id(db, artist_user.id)

    # Follow the artist
    client.post(
        f"/listeners/follow/{artist.name}",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    response = client.post(
        f"/listeners/follow/{artist.name}",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    # Assert the response status code
    assert response.status_code == 400
    assert response.json() == {"detail": "The listener follows the artist."}

    # Clean up the database
    db.delete(listener)
    db.delete(artist)
    db.commit()

# Test for unfollowing an artist
def test_unfollow_artist():
    db = next(get_db())

    # Create a random listener and artist
    listener_user = create_random_auth_listener(db)
    artist_user = create_random_auth_artist(db)

    listener = get_listener_by_user_id(db, listener_user.id)
    artist = get_artist_by_user_id(db, artist_user.id)

    # Follow the artist
    client.post(
        f"/listeners/follow/{artist.name}",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    response = client.post(
        f"/listeners/unfollow/{artist.name}",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert ListenerArtistLink table does not contain the listener-artist link
    follow = db.query(ListenerArtistLink).filter(
        ListenerArtistLink.listener_id == listener.listener_id,
        ListenerArtistLink.artist_id == artist.artist_id
    ).first()
    assert follow is None

    # Clean up the database
    db.delete(listener)
    db.delete(artist)
    db.commit()