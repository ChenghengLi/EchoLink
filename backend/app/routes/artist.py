from fastapi import APIRouter, Depends
from pytest import Session
from core.config import get_db
from crud.artist import get_all_artists
from models.artist import ArtistOutput
from typing import List

router = APIRouter()
    
@router.get("/", response_model=List[ArtistOutput])
def get_artists(db: Session = Depends(get_db)):
    """
    Retrieve all the artists from the database.
    """
    return get_all_artists(db)