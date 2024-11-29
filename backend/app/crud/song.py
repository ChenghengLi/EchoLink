from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.song import Song, SongInput, SongOutput
from models.artist import Artist
from models.user import User, RoleEnum
from crud.artist import get_artist_by_username

# Helper function to get a song or raise an error
def _get_song_or_error(db: Session, song_id: int) -> Song:
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song

# Get song by ID
def get_song_by_id(db: Session, song_id: int) -> SongOutput:
    song = _get_song_or_error(db, song_id)
    
    return SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=song.artist.user.username
    )

# Get songs by artist_id
def get_songs_by_artist_id(db: Session, artist_id: int):
    return db.query(Song).filter(Song.artist_id == artist_id).all()

def get_artist_by_song_id(db: Session, song_id: int) -> Artist:
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song.artist

# Get all songs
def get_all_songs(db: Session) -> list[SongOutput]:
    songs = db.query(Song).all()
    return [
        SongOutput(
            song_id=song.song_id,
            title=song.title,
            album=song.album,
            genre=song.genre,
            release_date=song.release_date,
            artist_name=song.artist.user.username
        )
        for song in songs
    ]

# Create a song
def create_song(db: Session, song_data: SongInput) -> SongOutput:
    artist = get_artist_by_username(db, song_data.artist_name)
    song = Song(
        title=song_data.title,
        album=song_data.album,
        genre=song_data.genre,
        release_date=song_data.release_date,
        artist_id=artist.artist_id
    )

    db.add(song)
    db.commit()
    db.refresh(song)

    return SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=artist.user.username
    )

# Update a song
def update_song(db: Session, song_id: int, song_data: SongInput) -> SongOutput:
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    
    artist = get_artist_by_username(db, song_data.artist_name)
    song.title = song_data.title
    song.album = song_data.album
    song.genre = song_data.genre
    song.release_date = song_data.release_date
    song.artist_id = artist.artist_id

    db.commit()
    db.refresh(song)

    return SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=artist.user.username
    )

# Delete a song
def delete_song(db: Session, song_id: int):
    song = _get_song_or_error(db, song_id)
    song_output = SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=song.artist.user.username
    )
    db.delete(song)
    db.commit()

    return song_output

# Check if an artist is the owner of a song
def is_artist_owner_song(db: Session, artist_id: int, song_id: int):
    song = _get_song_or_error(db, song_id)
    if song.artist_id != artist_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this song")
        
# Check of a user is an artist.
def is_user_artist(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user.role != RoleEnum.artist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an artist") 