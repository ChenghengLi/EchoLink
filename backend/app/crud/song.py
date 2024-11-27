from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.song import Song
from models.artist import Artist
from models.song import SongInput
from crud.artist import get_artist_by_username

# Get song by ID
def get_song_by_id(db: Session, song_id: int) -> Song:
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song

# Get songs by artist_id
def get_songs_by_artist_id(db: Session, artist_id: int):
    return db.query(Song).filter(Song.artist_id == artist_id).all()

# Get artist by song_id
def get_artist_by_song_id(db: Session, song_id: int) -> Artist:
    song = get_song_by_id(db, song_id)
    return song.artist

# Get all songs
def get_all_songs(db: Session):
    return db.query(Song).all()

# Create a song
def create_song(db: Session, song_data: SongInput) -> Song:
    artist = get_artist_by_username(db, song_data.artist_name)
    new_song = Song(
        title=song_data.title,
        album=song_data.album,
        genre=song_data.genre,
        release_date=song_data.release_date,
        artist_id=artist.artist_id
    )
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

# Update a song
def update_song(db: Session, song_id: int, song_data: SongInput) -> Song:
    song = get_song_by_id(db, song_id)
    song.title = song_data.title
    song.genre = song_data.genre
    song.album = song_data.album
    song.release_date = song_data.release_date
    db.commit()
    db.refresh(song)
    return song

# Delete a song
def delete_song(db: Session, song_id: int):
    song = get_song_by_id(db, song_id)
    db.delete(song)
    db.commit()
