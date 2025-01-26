import streamlit as st
from utils.api_utils import fetch_reddit_memes, fetch_giphy_gif, fetch_wikipedia_summary
from utils.gemini_utils import generate_response
from utils.chat_utils import initialize_chat_session, add_user_message, add_assistant_message, get_chat_context
from utils.personalization import get_user_preferences, update_preferences, add_interaction
from utils.trend_prediction import TrendPredictor
from dotenv import load_dotenv
import time

load_dotenv()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* Base styles */
.stApp {
    background: #1A1F2E;
    color: #F5F8FA;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Animated background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 0% 0%, #2C3E50, transparent 50%),
        radial-gradient(circle at 100% 0%, #3498DB, transparent 50%),
        radial-gradient(circle at 100% 100%, #2ECC71, transparent 50%),
        radial-gradient(circle at 0% 100%, #9B59B6, transparent 50%);
    animation: gradientMove 20s ease infinite;
    z-index: -1;
}

/* Enhanced title */
.stApp h1 {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem;
    margin-bottom: 1rem;
    text-align: center;
}

/* Chat message styling */
.chat-message {
    border-radius: 12px;
    padding: 16px;
    max-width: 90%;
    margin: 12px 0;
    animation: messageAppear 0.3s ease;
    background: rgba(55, 65, 81, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.chat-message:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.user-message {
    background: rgba(64, 75, 92, 0.7);
    margin-left: auto;
}

.assistant-message {
    background: rgba(55, 65, 81, 0.7);
    margin-right: auto;
}

/* Input field styling */
.stTextInput>div>div>input {
    background: rgba(55, 65, 81, 0.7);
    color: #F5F8FA;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 12px 16px;
    font-family: 'Inter', sans-serif;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}

/* Sidebar styling */
.sidebar .block-container {
    background: rgba(55, 65, 81, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(45deg, #4ECDC4, #556270);
    color: white;
    border-radius: 12px;
    padding: 8px 16px;
    transition: all 0.2s ease;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    border: none;
    position: relative;
    overflow: hidden;
}

.stButton>button::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: rotate(45deg);
    animation: glowEffect 3s infinite;
}

/* Animations */
@keyframes gradientMove {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

@keyframes messageAppear {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes glowEffect {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(29, 35, 51, 0.5);
}

::-webkit-scrollbar-thumb {
    background: rgba(75, 85, 99, 0.7);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(96, 107, 124, 0.7);
}

/* Trend prediction styling */
.trend-prediction {
    background: rgba(55, 65, 81, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px;
    animation: fadeIn 0.5s ease;
}

</style>
""", unsafe_allow_html=True)



if "trend_predictor" not in st.session_state:
   st.session_state.trend_predictor = TrendPredictor()

st.title("NoCap RAG")
st.write("Ask me anything, and I'll answer with memes and Gen Z wisdom!")

with st.sidebar:
   st.header("Preferences")
   favorite_memes = st.multiselect("Favorite Memes", ["Dog Memes", "Cat Memes", "Relatable Memes", "Pop Culture"], key="memes_select")
   favorite_topics = st.multiselect("Favorite Topics", ["Memes", "Pop Culture", "Trends", "Humor"], key="topics_select")
   if st.button("Save Preferences", key="save_prefs"):
       with st.spinner("Saving..."):
           time.sleep(0.3)
           update_preferences(favorite_memes, favorite_topics)
           st.success("✓")

if "chat_history" not in st.session_state:
   st.session_state.chat_history = initialize_chat_session()

for message in st.session_state.chat_history:
   if message["role"] != "system":
       with st.chat_message(message["role"]):
           message_class = "user-message" if message["role"] == "user" else "assistant-message"
           st.markdown(f'<div class="chat-message {message_class}">{message["content"]}</div>', unsafe_allow_html=True)
           if "image" in message:
               st.image(message["image"])

if user_query := st.chat_input("What's on your mind?"):
   st.session_state.chat_history = add_user_message(st.session_state.chat_history, user_query)
   with st.chat_message("user"):
       st.markdown(f'<div class="chat-message user-message">{user_query}</div>', unsafe_allow_html=True)

   with st.spinner(''):
       time.sleep(0.5)
       memes = fetch_reddit_memes(limit=3)
       gif_url = fetch_giphy_gif(user_query)
       wiki_summary = fetch_wikipedia_summary(user_query)

       context = get_chat_context(st.session_state.chat_history)
       if wiki_summary:
           context += f"\n\nWikipedia: {wiki_summary}"
       response = generate_response(user_query, context)

       st.session_state.chat_history = add_assistant_message(st.session_state.chat_history, response, gif_url)
       with st.chat_message("assistant"):
           st.markdown(f'<div class="chat-message assistant-message">{response}</div>', unsafe_allow_html=True)
           if gif_url:
               with st.container():
                   st.image(gif_url)

       add_interaction(user_query, response)

       for meme in memes:
           st.session_state.trend_predictor.add_data(meme["title"])

trends = st.session_state.trend_predictor.predict_trends()
if trends:
   st.markdown('<div class="trend-prediction">', unsafe_allow_html=True)
   st.write("### Trending Memes")
   for trend in trends:
       st.write(f"- {trend}")
   st.markdown('</div>', unsafe_allow_html=True)
