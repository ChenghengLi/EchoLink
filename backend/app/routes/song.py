from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.config import get_db
from core.security import get_current_user
from crud.song import get_song_by_id as get_song_by_id_crud, \
    get_all_songs as get_all_songs_crud, \
    create_song as create_song_crud, \
    update_song as update_song_crud, \
    delete_song as delete_song_crud, \
    is_artist_owner_song as is_artist_owner_song_crud, \
    is_user_artist as is_user_artist_crud
from crud.artist import get_artist_by_user_id
import models.song as song_model
import models.user as user_model

router = APIRouter()

# GET /songs -> Retrieve all songs
@router.get("/", response_model=list[song_model.SongOutput])
async def retrieve_all_songs(
    db: Session = Depends(get_db)
):
    return get_all_songs_crud(db)

# GET /songs/{song_id} -> Retrieve song by ID
@router.get("/{song_id}", response_model=song_model.SongOutput)
async def retrieve_song_by_id(
    song_id: int,
    db: Session = Depends(get_db)
):
    return get_song_by_id_crud(db, song_id)

# POST /songs -> Create a song
@router.post("/", response_model=song_model.SongOutput)
async def add_song(
    song_input: song_model.SongInput,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    is_user_artist_crud(db, current_user.id)

    return create_song_crud(db, song_input)

# PUT /songs/{song_id} -> Update a song
@router.put("/{song_id}", response_model=song_model.SongOutput)
async def update_song(
    song_id: int,
    song_update: song_model.SongInput,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    is_user_artist_crud(db, current_user.id)
    artist = get_artist_by_user_id(db, current_user.id)
    is_artist_owner_song_crud(db, artist.artist_id, song_id)

    return update_song_crud(db, song_id, song_update)

# DELETE /songs/{song_id} -> Delete a song
@router.delete("/{song_id}", status_code=status.HTTP_200_OK)
async def delete_song(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    is_user_artist_crud(db, current_user.id)
    artist = get_artist_by_user_id(db, current_user.id)
    is_artist_owner_song_crud(db, artist.artist_id, song_id)
    
    delete_song_crud(db, song_id)
    return {"message": "Song deleted successfully"}
