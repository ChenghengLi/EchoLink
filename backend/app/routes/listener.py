from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.listener import Listener
from crud.listener import follow_artist, unfollow_artist
from core.config import get_db
from core.security import CurrentUser

router = APIRouter()

# Follow an artist
@router.post("/follow/{artist_name}", status_code=200)
def follow_artist_route(
    artist_name: str,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    # Check if the current user is a listener
    listener = db.query(Listener).filter(Listener.user_id == current_user.id).first()
    if not listener:
        raise HTTPException(status_code=400, detail="You must be a listener to follow an artist.")
    
    print(listener)
    return follow_artist(db, listener, artist_name)

# Unfollow an artist
@router.post("/unfollow/{artist_name}", status_code=200)
def unfollow_artist_route(
    artist_name: str,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    # Check if the current user is a listener
    listener = db.query(Listener).filter(Listener.user_id == current_user.id).first()
    if not listener:
        raise HTTPException(status_code=400, detail="You must be a listener to unfollow an artist.")

    unfollow_artist(db, listener, artist_name)
