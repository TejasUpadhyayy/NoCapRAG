import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    model = genai.GenerativeModel('embedding-001')
    return model.embed_content(text)["embedding"]

def generate_response(prompt, context):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"{prompt}\n\nContext: {context}")
    return response.text