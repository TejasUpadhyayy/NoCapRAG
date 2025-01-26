import praw
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Dict, Any, Optional

load_dotenv()

def fetch_reddit_memes(limit: int = 3) -> List[Dict[str, Any]]:
   reddit = praw.Reddit(
       client_id=os.getenv("REDDIT_CLIENT_ID"),
       client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
       user_agent="mememind"
   )
   
   memes = []
   for post in reddit.subreddit('memes').hot(limit=limit):
       memes.append({
           'title': post.title,
           'url': post.url,
           'score': post.score
       })
   return memes

def fetch_giphy_gif(query: str) -> Optional[str]:
   api_key = os.getenv("GIPHY_API_KEY")
   url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=1"
   response = requests.get(url)
   data = response.json()
   return data['data'][0]['images']['original']['url'] if data.get('data') else None

def fetch_wikipedia_summary(query: str) -> Optional[str]:
   # Placeholder for Wikipedia integration
   return None

def generate_response(query: str, context: str = "") -> str:
   genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
   model = genai.GenerativeModel('gemini-pro')
   prompt = f"Context: {context}\nQuery: {query}" if context else query
   response = model.generate_content(prompt)
   return response.text
