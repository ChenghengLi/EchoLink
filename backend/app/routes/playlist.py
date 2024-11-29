from fastapi import APIRouter, Depends, status
from pytest import Session
from core.config import get_db
from core.security import CurrentUser
from typing import List
from models.playlist import PlaylistInput, PlaylistOutput, PlaylistUpdate
from crud.playlist import (
    get_playlist_by_id as get_playlist_by_id_crud,
    get_playlists as get_playlists_crud,
    get_playlists_by_username as get_playlists_by_username_crud,
    create_playlist as create_playlist_crud,
    update_playlist as update_playlist_crud,
    delete_playlist as delete_playlist_crud,
)

router = APIRouter()

@router.get("/", response_model=List[PlaylistOutput])
def get_playlists(
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all playlists.
    """
    return get_playlists_crud(db)

@router.get("/{playlist_id}", response_model=PlaylistOutput)
def get_playlist_by_id(
    playlist_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a playlist by ID.
    """
    return get_playlist_by_id_crud(db, playlist_id)

@router.get("/user/{username}", response_model=List[PlaylistOutput])
def get_playlists_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of playlists by username.
    """
    return get_playlists_by_username_crud(db, username)

@router.post("/", response_model=PlaylistOutput)
def create_playlist(
    playlist_data: PlaylistInput,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    print(current_user)
    print(playlist_data)
    """
    Create a new playlist.
    """
    return create_playlist_crud(db, playlist_data, current_user.id)

@router.put("/{playlist_id}", response_model=PlaylistOutput)
def update_playlist(
    playlist_id: int,
    update_data: PlaylistUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Update an existing playlist.
    """
    return update_playlist_crud(db, playlist_id, update_data, current_user.id)

@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(
    playlist_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Delete a playlist by ID.
    """
    delete_playlist_crud(db, playlist_id, current_user.id)
    return None
