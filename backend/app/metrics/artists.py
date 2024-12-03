
from crud.artist import get_followers, get_all_artists
from crud.question import get_questions_by_artist
from models.question import ResponseEnum
from pytest import Session


def reply_rate_score(artist_name: str, db: Session) -> float:
    # Fetch all questions for the artist
    all_questions = get_questions_by_artist(db, artist_name)

    # Total counts for each status
    answered = sum(1 for question in all_questions if question.response_status == ResponseEnum.answered)
    rejected = sum(1 for question in all_questions if question.response_status == ResponseEnum.rejected)
    waiting = sum(1 for question in all_questions if question.response_status == ResponseEnum.waiting)

    # Avoid division by zero
    if answered + rejected == 0:
        return 0.0  # No answered or rejected questions, rate is 0%

    # Calculate the answer rate
    answer_rate = (answered / (answered + rejected + waiting//2)) * 100

    # Return the rate rounded to 2 decimal places
    return round(answer_rate, 2)


def engage_artist_score(artist_name: str, db: Session) -> int:
    # Get the reply rate
    reply_rate = reply_rate_score(artist_name, db)  # Returns a percentage (0-100)

    # Get the number of followers
    followers = get_followers(db, artist_name)  # Returns an integer

    # Get all questions for the artist
    all_questions = get_questions_by_artist(db, artist_name)
    total_questions = len(all_questions) 

    # Calculate the weighted engagement score
    engage_score = 1000 + (reply_rate * 50) + (followers * 1.5) + (total_questions * 5)

    # Return the score as an integer
    return int(round(engage_score))


def get_my_ranking(artist_name: str, db: Session):

    # Get the engagement scores for all artists
    all_artists = get_all_artists(db)
    all_scores = {artist.username: engage_artist_score(artist.username, db) for artist in all_artists}

    # Sort the scores in descending order
    sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)

    # Initialize variables for ranking
    rank = 1
    previous_score = None
    artist_rank = None

    # Iterate through the sorted scores to assign ranks
    for i, (name, score) in enumerate(sorted_scores, start=1):
        # If the score is different from the previous score, update the rank
        if score != previous_score:
            rank = i
        # If the current artist matches the input artist, store their rank
        if name == artist_name:
            artist_rank = rank
        # Update the previous score
        previous_score = score

    # Return the rank of the artist
    return artist_rank
