from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.artist import Artist
from models.user import User, RoleEnum

# Get artist by user_id
def get_artist_by_user_id(db: Session, user_id: int) -> Artist:
    return db.query(Artist).filter(Artist.user_id == user_id).first()

# Create artist
def create_artist(db: Session, user: User) -> Artist:
    # Check if an artist already exists for this user
    if get_artist_by_user_id(db, user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already an artist.")

    # Create a new artist
    artist = Artist(
        user_id=user.id,
        name="TBD"
    )

    # Save to the database
    db.add(artist)
    db.commit()
    db.refresh(artist)

    return artist

# Get artist by username
def get_artist_by_username(db: Session, username: str) -> Artist:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    # Get artist by user_id
    artist = get_artist_by_user_id(db, user.id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not an artist.")
    
    return artist

# Get artists
def get_all_artists(db: Session):
    return db.query(User).filter(User.role == RoleEnum.artist).all()