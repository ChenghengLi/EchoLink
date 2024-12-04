
from models.artist import Artist
from pytest import Session
from crud.listener import get_listener_by_username

def loyalty_points(artist: Artist, listener_name: str, db: Session) -> int:
    listener = get_listener_by_username(db, listener_name)

    # TODO: CHANGE WITH ACTUAL BEHAVIOR IN ANOTHER TASK
    return listener.listener_id
