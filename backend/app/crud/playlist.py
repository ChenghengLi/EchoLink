from sqlalchemy.orm import Session
from models.playlist import Playlist, PlaylistInput, PlaylistUpdate
from typing import Optional

# Create a new playlist
def create_playlist(db: Session, playlist_data: PlaylistInput, user_id: int) -> Playlist:
    new_playlist = Playlist(
        name=playlist_data.name,
        description=playlist_data.description,
        visibility=playlist_data.visibility,
        user_id=user_id
    )
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return new_playlist

# Retrieve a playlist by ID
def get_playlist_by_id(db: Session, playlist_id: int) -> Optional[Playlist]:
    return db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()

# Update an existing playlist
def update_playlist(db: Session, playlist_id: int, update_data: PlaylistUpdate, user_id: int) -> Optional[Playlist]:
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()

    if playlist.user_id != user_id:
        raise ValueError("User does not have permission to update this playlist")

    if playlist:
        update_data = update_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(playlist, key, value)

        db.commit()
        db.refresh(playlist)
    
    return playlist

# Delete a playlist
def delete_playlist(db: Session, playlist_id: int, user_id: int) -> bool:
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()

    if playlist.user_id != user_id:
        raise ValueError("User does not have permission to delete this playlist")

    if playlist:
        db.delete(playlist)
        db.commit()
        return True
    return False
