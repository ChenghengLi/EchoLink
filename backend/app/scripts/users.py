import random
import json


questions = [
    # Creative Process and Inspiration
    "What inspires you the most when creating your art?",
    "How do you overcome creative blocks?",
    "Do you have a specific routine or ritual before starting a new project?",
    "What’s the most unusual source of inspiration you’ve ever had?",
    "How do you decide when a piece of art is finished?",
    "Do you prefer working in silence or with music? If music, what do you listen to?",
    "How do you stay motivated to create consistently?",
    "What’s your favorite medium to work with, and why?",
    "How do you experiment with new techniques or styles?",
    "Do you ever revisit old works and rework them?",

    # Personal Journey
    "When did you first realize you wanted to be an artist?",
    "Who was your biggest supporter when you started your career?",
    "What’s the first piece of art you ever created?",
    "How has your style evolved over the years?",
    "What’s the most significant lesson you’ve learned as an artist?",
    "Did you have any formal training, or are you self-taught?",
    "Who are your biggest artistic influences?",
    "What’s the best advice you’ve ever received about art?",
    "How do you handle criticism of your work?",
    "What’s the proudest moment of your career so far?",

    # Artistic Philosophy
    "What message do you hope people take away from your art?",
    "How do you define success as an artist?",
    "Do you believe art should always have a deeper meaning, or can it just be beautiful?",
    "How do you balance commercial success with staying true to your vision?",
    "What role do you think art plays in society?",
    "Do you think art should challenge people or comfort them?",
    "How do you feel about collaborations with other artists?",
    "What’s your opinion on the role of technology in modern art?",
    "Do you think art is something anyone can learn, or is it innate?",
    "How do you feel about the concept of 'art for art’s sake'?",

    # Career and Industry
    "What’s the hardest part about being an artist?",
    "How do you market yourself and your work?",
    "Have you ever faced rejection in your career? How did you handle it?",
    "What’s your favorite project you’ve ever worked on?",
    "How do you price your work?",
    "What’s the most challenging commission you’ve ever taken on?",
    "How do you feel about social media as a tool for artists?",
    "What’s your dream collaboration?",
    "How do you balance the business side of art with the creative side?",
    "What advice would you give to aspiring artists?",

    # Fun and Personal Questions
    "What’s your favorite color, and does it influence your work?",
    "If you weren’t an artist, what would you be doing?",
    "What’s your favorite piece of art by another artist?",
    "Do you collect art from other artists?",
    "What’s your favorite museum or gallery?",
    "If you could live in any era of art history, which would it be?",
    "What’s your favorite tool or material to work with?",
    "Do you have any quirky habits while creating?",
    "What’s the weirdest thing you’ve ever used in your art?",
    "If you could create art anywhere in the world, where would it be?",

    # Hypothetical and Imaginative Questions
    "If you could collaborate with any artist, living or dead, who would it be?",
    "If your art could come to life, what would it do?",
    "If you could only use one color for the rest of your life, which would it be?",
    "If you could design a public art installation, what would it look like?",
    "If you could turn one of your pieces into a movie, which one would it be?",
    "If you could teach a class on art, what would the first lesson be?",
    "If you could create art for a famous person, who would it be?",
    "If you could only create one type of art for the rest of your life, what would it be?",
    "If you could have any superpower to help with your art, what would it be?",
    "If you could exhibit your work anywhere in the world, where would it be?",

    # Art and Emotions
    "How does your mood affect your art?",
    "Do you think art can heal emotional wounds?",
    "What’s the most emotional piece you’ve ever created?",
    "How do you express joy in your art?",
    "How do you express sadness or anger in your art?",
    "Do you think art can change the way people feel?",
    "How do you handle the vulnerability of sharing your art with others?",
    "What’s the most personal piece of art you’ve ever made?",
    "How do you feel when someone connects deeply with your work?",
    "Do you think art can bring people together?",

    # Artistic Challenges
    "What’s the biggest challenge you’ve faced as an artist?",
    "How do you deal with self-doubt?",
    "Have you ever felt like giving up on art? What kept you going?",
    "How do you handle deadlines for commissioned work?",
    "What’s the longest you’ve ever worked on a single piece?",
    "How do you deal with perfectionism in your work?",
    "What’s the most frustrating part of the creative process?",
    "How do you handle negative feedback or reviews?",
    "Have you ever had a piece of art fail? What did you learn from it?",
    "How do you stay inspired during tough times?",

    # Future and Legacy
    "What’s your ultimate goal as an artist?",
    "How do you want to be remembered as an artist?",
    "What’s a dream project you haven’t done yet?",
    "Where do you see your art in 10 years?",
    "Do you think your art will outlive you?",
    "How do you want your art to impact the world?",
    "What’s the next big thing you’re working on?",
    "Do you mentor or teach other artists?",
    "How do you think the art world will change in the future?",
    "What’s one thing you hope never changes about art?",

    # Rapid-Fire Fun Questions
    "Oil or acrylic?",
    "Abstract or realism?",
    "Morning or night for creating?",
    "Sketchbook or canvas?",
    "Digital or traditional art?",
    "Favorite art supply brand?",
    "Favorite art movement?",
    "Favorite snack while working?",
    "Most-used color in your palette?",
    "One word to describe your art?"
]


filename = 'backend/app/data/top_artists.json'

with open(filename, 'r', encoding='utf-8') as f:
    artists = json.load(f)


artists = [artist['name'] for artist in artists]

# List of first names
first_names = [
    "John", "Jane", "Alice", "Bob", "Eve", "Frank", 
    "Grace", "Hank", "Ivy", "Jack", "Karen", "Leo", 
    "Mona", "Nina", "Oscar", "Paul", "Steve", "Tina", 
    "Uma", "Victor", "Wendy", "Yara", "Zane"
]

# List of surnames
surnames = [
    "Smith", "Brown", "Jones", "Miller", "Davis", 
    "Moore", "Martin", "Clark", "Lewis", "Walker", 
    "White", "Perez", "Taylor", "Lopez", "Wilson", 
    "Thomas", "Harris", "Sanchez", "Garcia", "Jackson"
]

# Number of users to generate
n = 100

# Dictionary to store user data
user_data = {}

# Generate random usernames, emails, passwords, followers, and questions
for _ in range(n):
    # Randomly select a first name and a surname
    first_name = random.choice(first_names)
    surname = random.choice(surnames)
    # Create username by combining first name and surname
    username = f"{first_name}{surname}"
    # Create email and convert it to lowercase
    email = f"{username}@test.com".lower()
    # Set password
    password = "password"
    # Generate a random number of followed artists (1 to 50)
    num_followed_artists = random.randint(1, 50)
    followed_artists = random.sample(artists, num_followed_artists)

    num_questions = random.randint(1, num_followed_artists)

    # Generate questions for a random subset of followed artists
    artist_questions = {}	

    for _ in range(num_questions):
        # Randomly select an artist
        artist = random.choice(followed_artists)
        artist_questions[artist] = random.choice(questions)

    # Store in dictionary
    user_data[username] = {
        "username": username,
        "email": email,
        "password": password,
        "followers": followed_artists,
        "artist_questions": artist_questions
    }

# Print the resulting dictionary
# Define the file path
file_path = "backend/app/data/user.json"

# Write the user data to the JSON file
with open(file_path, "w") as json_file:
    json.dump(user_data, json_file, indent=4)