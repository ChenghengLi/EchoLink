from fastapi import APIRouter, Depends, HTTPException, status
from pytest import Session
from core.config import get_db
from core.security import CurrentUser
from typing import List
from models.question import ResponseEnum, QuestionModel, QuestionInput, QuestionResponse
from crud.question import (
    get_questions_by_listener,
    get_questions_by_artist,
    submit_question,
    response_question
)
from crud.listener import get_listener_by_username
from crud.artist import get_artist_by_username

router = APIRouter()
    
@router.get("/questions", response_model=List[QuestionModel])
def get_questions(user: CurrentUser, db: Session = Depends(get_db)):
    """
    Retrieve questions for a listener or artist (the user is derived from the Authorization token).
    """
    try:
        # If the user is a listener, return questions
        return get_questions_by_listener(db, user.username)
        
    except Exception:
        # If not, try to get questions for an artist
        try:
            return get_questions_by_artist(db, user.username)
        
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user is neither a listener nor an artist."
            )


@router.post("/questions", response_model=QuestionModel)
def create_question(question_input: QuestionInput, user: CurrentUser, db: Session = Depends(get_db)):
    """
    Submit a new question to an artist (the listener is derived from the Authorization token).
    """
    return submit_question(db, get_listener_by_username(db, user.username), question_input)


@router.post("/questions/reject", response_model=QuestionModel)
def reject_question_endpoint(response: QuestionResponse, user: CurrentUser, db: Session = Depends(get_db)):
    """
    Reject a question by its ID (it must be assigned to the artist derived from the Authorization token).
    """
    return response_question(db, get_artist_by_username(db, user.username), 
                             response, response_status=ResponseEnum.rejected)


@router.post("/questions/answer", response_model=QuestionModel)
def answer_question_endpoint(response: QuestionResponse, user: CurrentUser, db: Session = Depends(get_db)):
    """
    Answer a question by its ID (it must be assigned to the artist derived from the Authorization token).
    """
    return response_question(db, get_artist_by_username(db, user.username), 
                             response, response_status=ResponseEnum.answered)
