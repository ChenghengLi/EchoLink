import pytest
from datetime import datetime
from models.question import Question, QuestionInput, QuestionResponse, ResponseEnum
from crud.question import get_questions_by_listener, get_questions_by_artist, submit_question, get_question_by_id, response_question, reject_question, answer_question
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

# Test: Get questions by listener username
def test_get_questions_by_listener(db_session):
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    retrieved_questions = get_questions_by_listener(db_session, listener.user.username)
    assert len(retrieved_questions) > 0
    assert retrieved_questions[0].listener_id == listener.listener_id

# Test: Get questions by artist username
def test_get_questions_by_artist(db_session):
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    retrieved_questions = get_questions_by_artist(db_session, artist.user.username)
    assert len(retrieved_questions) > 0
    assert retrieved_questions[0].artist_id == artist.artist_id

# Test: Submit a question
def test_submit_question(db_session):
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)

    question_input = QuestionInput(
        listener_username=listener.user.username,
        artist_username=artist.user.username,
        question_text="What is your favorite song?"
    )

    question = submit_question(db_session, question_input)
    db_session.refresh(question)

    assert question.listener_id == listener.listener_id
    assert question.artist_id == artist.artist_id
    assert question.question_text == "What is your favorite song?"
    assert question.response_status == ResponseEnum.waiting

# Test: Get question by id
def test_get_question_by_id(db_session):
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    retrieved_question = get_question_by_id(db_session, question.question_id)
    assert retrieved_question is not None
    assert retrieved_question.question_id == question.question_id

# Test: Response to a question
def test_response_question(db_session):
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    response = QuestionResponse(question_id=question.question_id, response_text="I love this song!")
    answered_question = response_question(db_session, response, ResponseEnum.answered)

    assert answered_question.response_status == ResponseEnum.answered
    assert answered_question.response_text == "I love this song!"

# Test: Reject a question
def test_reject_question(db_session):
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    response = QuestionResponse(question_id=question.question_id, response_text="I don't want to answer.")
    rejected_question = reject_question(db_session, response)

    assert rejected_question.response_status == ResponseEnum.rejected
    assert rejected_question.response_text == "I don't want to answer."

# Test: Answer a question
def test_answer_question(db_session):
    listener = create_random_listener(db_session)
    artist = create_random_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    response = QuestionResponse(question_id=question.question_id, response_text="My favorite song is XYZ.")
    answered_question = answer_question(db_session, response)

    assert answered_question.response_status == ResponseEnum.answered
    assert answered_question.response_text == "My favorite song is XYZ."
