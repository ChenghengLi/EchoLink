from sqlalchemy.orm import Session
from datetime import datetime
from models.question import Question, QuestionInput, QuestionResponse, ResponseEnum
from fastapi import HTTPException, status
from crud.artist import get_artist_by_username
from crud.listener import get_listener_by_username

# Get questions by listener username
def get_questions_by_listener(db: Session, username: str):
    listener = get_listener_by_username(db, username)
    return db.query(Question).filter(Question.listener_id == listener.listener_id).all()

# Get questions by artist username
def get_questions_by_artist(db: Session, username: str):
    artist = get_artist_by_username(db, username)
    return db.query(Question).filter(Question.artist_id == artist.artist_id).all()

# Add a new question to the database
def submit_question(db: Session, question_input: QuestionInput) -> Question:
    listener = get_listener_by_username(db, question_input.listener_username)
    artist = get_artist_by_username(db, question_input.artist_username)

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

# Response a existing question
def response_question(db: Session, response: QuestionResponse, response_status: ResponseEnum):
    question = get_question_by_id(db, response.question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
    
    question.response_text = response.response_text
    question.response_date = datetime.utcnow()
    question.response_status = response_status
    db.commit()
    db.refresh(question)
    return question

# Reject a question
def reject_question(db: Session, response: QuestionResponse):
    return response_question(db, response, ResponseEnum.rejected)

# Answer a question
def answer_question(db: Session, response: QuestionResponse):
    return response_question(db, response, ResponseEnum.answered)
    