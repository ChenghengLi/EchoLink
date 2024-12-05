from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.listener import Listener
from models.user import ListenerArtistLink, RoleEnum, User
from crud.artist import get_artist_by_username

# Get listener by user_id
def get_listener_by_user_id(db: Session, user_id: int) -> Listener:
    return db.query(Listener).filter(Listener.user_id == user_id).first()

# Create listener
def create_listener(db: Session, user: User) -> Listener:
    # Check if a listener already exists for this user
    if get_listener_by_user_id(db, user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already a listener.")

    # Create a new listener
    listener = Listener(user_id=user.id)

    # Save to the database
    db.add(listener)
    db.commit()
    db.refresh(listener)

    return listener

# Get listeners
def get_all_listeners(db: Session):
    return db.query(User).filter(User.role == RoleEnum.listener).all()

# Get listener by username
def get_listener_by_username(db: Session, username: str) -> Listener:
    # Get user by username
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    # Get listener by user_id
    listener = get_listener_by_user_id(db, user.id)
    if not listener:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not a listener.")
    
    return listener


def check_follow(db: Session, listener: Listener, artist_username: str) -> bool:
    artist = get_artist_by_username(db, artist_username)
    return db.query(ListenerArtistLink).filter(
        ListenerArtistLink.listener_id == listener.listener_id,
        ListenerArtistLink.artist_id == artist.artist_id
    ).first() is not None


# Follow an artist
def follow_artist(db: Session, listener: Listener, artist_username: str) -> ListenerArtistLink:
    artist = get_artist_by_username(db, artist_username)

    # Check if the listener is already following the artist
    existing_follow = db.query(ListenerArtistLink).filter(
        ListenerArtistLink.listener_id == listener.listener_id,
        ListenerArtistLink.artist_id == artist.artist_id
    ).first()
    if existing_follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The listener follows the artist.")

    # Create the follow link
    follow_link = ListenerArtistLink(listener_id=listener.listener_id, artist_id=artist.artist_id)
    db.add(follow_link)
    db.commit()
    db.refresh(follow_link)

    return follow_link

# Unfollow an artist
def unfollow_artist(db: Session, listener: Listener, artist_username: str):
    artist = get_artist_by_username(db, artist_username)

    # Check if the listener is following the artist
    follow = db.query(ListenerArtistLink).filter(
        ListenerArtistLink.listener_id == listener.listener_id,
        ListenerArtistLink.artist_id == artist.artist_id
    ).first()
    if not follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The listener does not follow the artist.")

    # Delete the follow link
    db.delete(follow)
    db.commit()