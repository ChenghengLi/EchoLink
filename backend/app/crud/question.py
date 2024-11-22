from sqlalchemy.orm import Session
from datetime import datetime
from models.question import Question, QuestionInput, QuestionResponse, ResponseEnum
from fastapi import HTTPException, status
from crud.artist import get_artist_by_username
from crud.listener import get_listener_by_username
from models.listener import Listener
from models.artist import Artist

# Get questions by listener username
def get_questions_by_listener(db: Session, username: str):
    listener = get_listener_by_username(db, username)
    return db.query(Question).filter(Question.listener_id == listener.listener_id).all()

# Get questions by artist username
def get_questions_by_artist(db: Session, username: str):
    artist = get_artist_by_username(db, username)
    return db.query(Question).filter(Question.artist_id == artist.artist_id).all()

# Decide if a listener can ask a question to an artist
def can_question(db: Session, listener: Listener, artist: Artist):
    # TODO: Implement algorithm based on metrics
    return True

# Add a new question to the database
def submit_question(db: Session, listener: Listener, question_input: QuestionInput) -> Question:
    artist = get_artist_by_username(db, question_input.artist_username)

    # Decide if the listener can ask a question to the artist
    if not can_question(db, listener, artist):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This listener cannot ask this artist.")
    
    # Check if a question the listener is waiting for a response from the artist
    if db.query(Question).filter(Question.listener_id == listener.listener_id, 
                                 Question.artist_id == artist.artist_id,
                                 Question.response_status == ResponseEnum.waiting).first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This listener is waiting for a response.")

    # Create Question
    question = Question(
        listener_id=listener.listener_id,
        artist_id=artist.artist_id,
        question_text=question_input.question_text,
        response_status = ResponseEnum.waiting,
        question_date=datetime.utcnow()
    )

    # Add question to the session and commit it
    db.add(question)
    db.commit()
    db.refresh(question)

    return question

# Get a question by its id
def get_question_by_id(db: Session, question_id: int):
    return db.query(Question).filter(Question.question_id == question_id).first()

# Response a question from an artist
def response_question(db: Session, artist: Artist, response: QuestionResponse, response_status: ResponseEnum) -> Question:
    question = get_question_by_id(db, response.question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
    
    if question.artist_id != artist.artist_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This artist cannot answer this question.")
    
    if question.response_status != ResponseEnum.waiting:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This question has already been responded.")
    
    # Update question
    question.response_text = response.response_text
    question.response_date = datetime.utcnow()
    question.response_status = response_status
    db.commit()
    db.refresh(question)
    return question
    