import os
import praw
import requests
import wikipedia
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reddit API setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="mememind"
)

# Giphy API setup
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

def fetch_reddit_memes(subreddit="memes", limit=5):
    """Fetch trending memes from Reddit."""
    memes = []
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        memes.append({
            "title": submission.title,
            "url": submission.url,
            "score": submission.score
        })
    return memes

def fetch_giphy_gif(query):
    """Fetch a relevant GIF from Giphy."""
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=1"
    response = requests.get(url).json()
    if response["data"]:
        return response["data"][0]["images"]["original"]["url"]
    return None

def fetch_wikipedia_summary(query):
    """Fetch a summary from Wikipedia."""
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=2)
    except wikipedia.exceptions.PageError:
        return None