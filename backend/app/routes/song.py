from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.config import get_db
from crud.song import get_song_by_id as get_song_by_id_crud, \
    get_all_songs as get_all_songs_crud, \
    create_song as create_song_crud, \
    update_song as update_song_crud, \
    delete_song as delete_song_crud
import models.song as song_model

router = APIRouter()

# GET /songs -> Retrieve all songs
@router.get("/", response_model=list[song_model.SongOutput])
async def retrieve_all_songs(
    db: Session = Depends(get_db)
):
    songs = get_all_songs_crud(db)
    return [song_model.SongOutput.model_validate(song) for song in songs]

# GET /songs/{song_id} -> Retrieve song by ID
@router.get("/{song_id}", response_model=song_model.SongOutput)
async def retrieve_song_by_id(
    song_id: int,
    db: Session = Depends(get_db)
):
    song = get_song_by_id_crud(db, song_id)
    return song_model.SongOutput.model_validate(song)

# POST /songs -> Create a song
@router.post("/", response_model=song_model.SongOutput)
async def add_song(
    song_input: song_model.SongInput,
    db: Session = Depends(get_db)
):
    song = create_song_crud(db, song_input)
    return song_model.SongOutput.model_validate(song)

# PUT /songs/{song_id} -> Update a song
@router.put("/{song_id}", response_model=song_model.SongOutput)
async def update_song(
    song_id: int,
    song_update: song_model.SongInput,
    db: Session = Depends(get_db)
):
    song = update_song_crud(db, song_id, song_update)
    return song_model.SongOutput.model_validate(song)

# DELETE /songs/{song_id} -> Delete a song
@router.delete("/{song_id}", status_code=status.HTTP_200_OK)
async def delete_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    delete_song_crud(db, song_id)
    return {"message": "Song deleted successfully"}

