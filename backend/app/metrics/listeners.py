
from models.playlist import Playlist
from models.question import Question
from models.artist import Artist
from pytest import Session
from crud.listener import get_listener_by_username, check_follow

def loyalty_points(artist: Artist, listener_name: str, db: Session) -> int:
    listener = get_listener_by_username(db, listener_name)

    # Check if the listener follows the artist
    follow_score = 5000 if check_follow(db, listener, artist.user.username) else 0

    # Questions from the listener to the artist
    questions = db.query(Question).filter(Question.artist_id == artist.artist_id, 
                                          Question.listener_id == listener.listener_id).all()
    
    # Calculate the score based on the number of questions (small, increase the value with answer/reject rate)
    question_score = 20 * len(questions)

    # Answered questions give more points
    answer_score = 1000 * sum(1 for question in questions if question.response_status == "answered")

    # Rejected questions reduce the score
    reject_score = -200 * sum(1 for question in questions if question.response_status == "rejected")

    # Playlists with artist's songs give points (based on the % of songs of the artist)
    playlists = db.query(Playlist).filter(Playlist.user_id == listener.user_id).all()
    playlist_score = 0
    for playlist in playlists:
        artist_songs = sum(1 for song in playlist.songs if song.artist_id == artist.artist_id)
        playlist_score += 50 * artist_songs / len(playlist.songs)

    # Check if the listener's favorite genre matches the artist's genre
    genre_score = 100 if listener.user.genre == artist.user.genre else 0

    # Combine the scores
    loyalty_score = follow_score + question_score + answer_score + reject_score + playlist_score + genre_score

    # Return a score as an integer (minimum 1000)
    return 1000 + max(int(round(loyalty_score)), 0)
