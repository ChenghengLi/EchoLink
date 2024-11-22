import pytest
from datetime import datetime
from fastapi import HTTPException, status
from models.question import Question, QuestionInput, QuestionResponse, ResponseEnum
from crud.question import submit_question, response_question
from tests.utils import create_random_artist, create_random_listener, get_session

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a clean database session for each test.
    Automatically rolls back transactions after each test.
    """
    db = get_session()  # Assume get_session() provides a valid SQLAlchemy session
    try:
        yield db
    finally:
        db.rollback()
        db.close()

def test_submit_question_when_waiting_for_response(db_session):
    # Arrange: Create a listener, artist, and a question that is already waiting for a response
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)
    
    # Create an existing question with the 'waiting' status
    question_input = QuestionInput(
        listener_username=listener.user.username,
        artist_username=artist.user.username,
        question_text="What is your favorite song?"
    )
    submit_question(db_session, listener, question_input)  # Submit the first question
    
    # Act: Try submitting another question while waiting for a response
    new_question_input = QuestionInput(
        listener_username=listener.user.username,
        artist_username=artist.user.username,
        question_text="Another question?"
    )

    # Act & Assert: Check that HTTPException is raised
    with pytest.raises(HTTPException) as exc_info:
        submit_question(db_session, listener, new_question_input)
    
    assert exc_info.value.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert exc_info.value.detail == "This listener is waiting for a response."


### Test Cases for `response_question`

def test_response_question_when_artist_not_allowed_to_respond(db_session):
    # Arrange: Create listener, artist, and a question that doesn't belong to the artist
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)
    other_artist = create_random_artist(db_session)  # Another artist
    
    question = Question(
        listener_id=listener.listener_id,
        artist_id=artist.artist_id,
        question_text="What is your favorite song?",
        question_date=datetime.utcnow(),
        response_status=ResponseEnum.waiting
    )
    db_session.add(question)
    db_session.commit()

    # Create a response for a different artist
    response = QuestionResponse(
        question_id=question.question_id,
        response_text="I love this song!"
    )

    # Act & Assert: Check that HTTPException is raised because artist is not the correct one
    with pytest.raises(HTTPException) as exc_info:
        response_question(db_session, other_artist, response, ResponseEnum.answered)
    
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "This artist cannot answer this question."


def test_response_question_when_already_answered(db_session):
    # Arrange: Create listener, artist, and a question that has already been answered
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)
    
    question = Question(
        listener_id=listener.listener_id,
        artist_id=artist.artist_id,
        question_text="What is your favorite song?",
        question_date=datetime.utcnow(),
        response_status=ResponseEnum.answered,  # Already answered
        response_text="I love this song!"
    )
    db_session.add(question)
    db_session.commit()

    response = QuestionResponse(
        question_id=question.question_id,
        response_text="Another response"
    )

    # Act & Assert: Check that HTTPException is raised because the question has already been answered
    with pytest.raises(HTTPException) as exc_info:
        response_question(db_session, artist, response, ResponseEnum.answered)
    
    assert exc_info.value.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert exc_info.value.detail == "This question has already been responded."


def test_response_question_successful(db_session):
    # Arrange: Create listener, artist, and a question that is waiting for a response
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)
    
    question = Question(
        listener_id=listener.listener_id,
        artist_id=artist.artist_id,
        question_text="What is your favorite song?",
        question_date=datetime.utcnow(),
        response_status=ResponseEnum.waiting  # Waiting for response
    )
    db_session.add(question)
    db_session.commit()

    response = QuestionResponse(
        question_id=question.question_id,
        response_text="My favorite song is XYZ"
    )

    # Act: Respond to the question
    answered_question = response_question(db_session, artist, response, ResponseEnum.answered)

    # Assert: Check that the response was successfully added
    assert answered_question.response_status == ResponseEnum.answered
    assert answered_question.response_text == "My favorite song is XYZ"
    assert answered_question.response_date is not None
