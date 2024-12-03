from fastapi import APIRouter, Depends
from metrics.artists import reply_rate_score, engage_artist_score, get_my_ranking
from crud.artist import get_followers
from pytest import Session
from core.config import get_db

router = APIRouter()

@router.get("/response_rate", response_model=float)
def get_artist_reply_rate(artist_name: str, db: Session = Depends(get_db)) -> float:
    """
    Calculate and return the reply rate of an artist.

    The reply rate is a metric that measures how frequently the artist responds to questions or interactions.

    Args:
        artist (Artist): The artist object containing data about their interactions and responses.

    Returns:
        float: The reply rate of the artist as a floating-point number.
    """
    return reply_rate_score(artist_name, db)


@router.get("/engagement_rate", response_model=float)
def get_artist_engagement_rate(artist_name: str, db: Session = Depends(get_db)) -> float:
    """
    Calculate and return the engagement rate of an artist.

    The engagement rate evaluates how actively the artist interacts with their audience, factoring in their responses and follower base.

    Args:
        artist (Artist): The artist object containing data about their interactions, responses, and followers.

    Returns:
        float: The engagement rate of the artist as a floating-point number.
    """
    return engage_artist_score(artist_name, db)


@router.get("/followers", response_model=int)
def get_artist_followers(artist_name: str, db: Session = Depends(get_db)) -> int:
    """
    Retrieve and return the total number of followers for an artist.

    The number of followers is a key metric that reflects the size of the artist's audience.

    Args:
        artist (Artist): The artist object containing data about their profile and audience.

    Returns:
        int: The total number of followers the artist has as an integer.
    """
    return get_followers(db, artist_name)



@router.get("/ranking", response_model=int)
def get_artist_ranking(artist_name: str, db: Session = Depends(get_db)) -> int:
    """
    Retrieve and return the ranking for an artist.

    The number of followers is a key metric that reflects the size of the artist's audience.

    Args:
        artist (Artist): The artist object containing data about their profile and audience.

    Returns:
        int: The total number of followers the artist has as an integer.
    """
    return get_my_ranking(artist_name, db)