from fastapi import APIRouter, Depends
from pytest import Session
from core.config import get_db
from crud.artist import get_all_artists, get_followers
from models.user import UserOutput
from typing import List
from metrics.artists import engage_artist_score

router = APIRouter()
    
@router.get("/", response_model=List[UserOutput])
def get_artists_alphabet(db: Session = Depends(get_db)):
    """
    Retrieve all the artists from the database by alphabet
    """
    artists_list = get_all_artists(db)
    artists_list.sort(key=lambda x: x.username)
    print(artists_list)
    return artists_list

@router.get("/engagement", response_model=List[UserOutput])
def get_artists_engagement(db: Session = Depends(get_db)):
    """
    Retrieve all the artists from the database by engagement
    """
    artists_list = get_all_artists(db)
    artists_list.sort(key=lambda x: engage_artist_score(x.username, db))
    return artists_list


@router.get("/followers", response_model=List[UserOutput])
def get_artists_followers(db: Session = Depends(get_db)):
    """
    Retrieve all the artists from the database.
    """
    artists_list = get_all_artists(db)
    artists_list.sort(key=lambda x: get_followers(db, x.username))
    return artists_list