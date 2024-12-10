from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.song import Song, SongInput, SongOutput, SongSource
from models.artist import Artist
from models.user import ListenerArtistLink, User, RoleEnum
from crud.artist import get_artist_by_username
from crud.listener import get_listener_by_user_id
import random

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
        artist_name=song.artist.user.username,
        sources=song.source_urls
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
            artist_name=song.artist.user.username,
            sources=song.source_urls
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

    # Add song sources (now song_id is assigned)
    song.sources = [SongSource(song_id=song.song_id, source_url=str(url)) for url in song_data.sources]

    return SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=artist.user.username,
        sources=song.source_urls
    )

# Update a song
def update_song(db: Session, song_id: int, song_data: SongInput) -> SongOutput:
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    
    # Clear existing sources
    db.query(SongSource).filter(SongSource.song_id == song.song_id).delete()
    db.commit()
    
    artist = get_artist_by_username(db, song_data.artist_name)
    song.title = song_data.title
    song.album = song_data.album
    song.genre = song_data.genre
    song.release_date = song_data.release_date
    song.artist_id = artist.artist_id

    # Update with new sources
    song.sources = [SongSource(song_id=song.song_id, source_url=str(url)) for url in song_data.sources]

    db.commit()
    db.refresh(song)

    return SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=artist.user.username,
        sources=song.source_urls
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
        artist_name=song.artist.user.username,
        sources = []
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

def get_recommendations(db: Session, user: User) -> list[Song]:
    # Check if the user is a listener
    listener = get_listener_by_user_id(db, user.id)
    if not listener:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not a listener.")
    
    # Step 0: Check if database has at least 10 songs, otherwise return all songs
    song_count = db.query(Song).count()
    if song_count < 10:
        return db.query(Song).all()

    # Step 1: Get songs by followed artists
    followed_artists = (
        db.query(Artist.artist_id)
        .join(ListenerArtistLink, ListenerArtistLink.artist_id == Artist.artist_id)
        .filter(ListenerArtistLink.listener_id == listener.listener_id)
        .all()
    )
    followed_songs = (
        db.query(Song)
        .filter(Song.artist_id.in_([artist.artist_id for artist in followed_artists]))
        .all()
    )

    # If there are 30 or more songs, pick 10 at random
    if len(followed_songs) >= 30:
        return random.sample(followed_songs, 10)

    # Step 2: Add songs with the listener's preferred genre
    genres = db.query(Song.genre).filter(Song.artist_id.in_([artist.artist_id for artist in followed_artists])).distinct().all()
    genres = [genre[0] for genre in genres]
    genres_songs = (
        db.query(Song)
        .filter(Song.genre.in_(genres))
        .all()
    )

    combined_list = list(set(followed_songs + genres_songs))

    # If the combined list has 30 or more songs, pick 10 at random
    if len(combined_list) >= 30:
        return random.sample(combined_list, 10)

    # Step 3: Handle small lists
    selected_songs = random.sample(combined_list, min(5, len(combined_list)))

    # Add random songs from the database excluding already selected ones
    remaining_songs = (
        db.query(Song)
        .filter(~Song.song_id.in_([song.song_id for song in combined_list]))
        .all()
    )
    additional_songs = random.sample(remaining_songs, 10 - len(selected_songs))
    return selected_songs + additional_songs