from fastapi import APIRouter, Depends
from pytest import Session
from core.config import get_db
from crud.artist import get_followers
from models.artist import ArtistOutput
from typing import List
from metrics.artists import engage_artist_score, get_all_artists_with_rank_data

router = APIRouter()
    
@router.get("/", response_model=List[ArtistOutput])
def get_artists_alphabet(db: Session = Depends(get_db)):
    """
    Retrieve all the artists from the database by alphabet
    """
    artists_list = get_all_artists_with_rank_data(db)
    artists_list.sort(key=lambda x: x.username)
    print(artists_list)
    return artists_list

@router.get("/engagement", response_model=List[ArtistOutput])
def get_artists_engagement(db: Session = Depends(get_db)):
    """
    Retrieve all the artists from the database by engagement
    """
    artists_list = get_all_artists_with_rank_data(db)
    artists_list.sort(key=lambda x: engage_artist_score(x.username, db), reverse=True)
    return artists_list


@router.get("/followers", response_model=List[ArtistOutput])
def get_artists_followers(db: Session = Depends(get_db)):
    """
    Retrieve all the artists from the database.
    """
    artists_list = get_all_artists_with_rank_data(db)
    artists_list.sort(key=lambda x: get_followers(db, x.username), reverse=True)
    return artists_list