from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.artist import Artist, ArtistInput
from crud.user import get_user_by_username

# Get artist by user_id
def get_artist_by_user_id(db: Session, user_id: int) -> Artist:
    return db.query(Artist).filter(Artist.user_id == user_id).first()

# Create artist
def create_artist(db: Session, artist_input: ArtistInput) -> Artist:
    # Get the user by username
    user = get_user_by_username(db, artist_input.username)

    # Check if an artist already exists for this user
    if get_artist_by_user_id(db, user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already an artist.")

    # Create a new artist
    artist = Artist(
        user_id=user.id,
        name=artist_input.name,
        genre=artist_input.genre,
        bio=artist_input.bio
    )

    # Save to the database
    db.add(artist)
    db.commit()
    db.refresh(artist)

    return artist

# Get artist by username
def get_artist_by_username(db: Session, username: str) -> Artist:
    # Get user by username
    user = get_user_by_username(db, username)
    
    # Get artist by user_id
    artist = get_artist_by_user_id(db, user.id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not an artist.")
    
    return artist
