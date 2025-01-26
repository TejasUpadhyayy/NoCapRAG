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

.stApp {
   background: #1A1F2E;
   color: #F5F8FA;
   font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

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
}

.user-message {
   background: rgba(64, 75, 92, 0.7);
   margin-left: auto;
}

.assistant-message {
   background: rgba(55, 65, 81, 0.7);
   margin-right: auto;
}

.stTextInput>div>div>input {
   background: rgba(55, 65, 81, 0.7);
   color: #F5F8FA;
   border: 1px solid rgba(255, 255, 255, 0.1);
   border-radius: 8px;
   padding: 12px 16px;
   font-family: 'Inter', sans-serif;
   backdrop-filter: blur(12px);
   -webkit-backdrop-filter: blur(12px);
}

.sidebar .block-container {
   background: rgba(55, 65, 81, 0.7);
   backdrop-filter: blur(12px);
   -webkit-backdrop-filter: blur(12px);
   border: 1px solid rgba(255, 255, 255, 0.1);
   border-radius: 12px;
   padding: 16px;
}

.stButton>button {
   background: rgba(59, 130, 246, 0.8);
   color: white;
   border-radius: 6px;
   padding: 8px 16px;
   transition: all 0.2s ease;
   font-family: 'Inter', sans-serif;
   font-weight: 500;
   border: 1px solid rgba(255, 255, 255, 0.1);
}

.stButton>button:hover {
   background: rgba(37, 99, 235, 0.8);
}

.trend-prediction {
   background: rgba(55, 65, 81, 0.7);
   backdrop-filter: blur(12px);
   -webkit-backdrop-filter: blur(12px);
   border: 1px solid rgba(255, 255, 255, 0.1);
   border-radius: 12px;
   padding: 16px;
}

h1, h2, h3, .stTitle {
   font-family: 'Inter', sans-serif;
   font-weight: 600;
   letter-spacing: -0.02em;
   color: #F5F8FA !important;
}

header {
   background: rgba(26, 31, 46, 0.95) !important;
   backdrop-filter: blur(12px);
   -webkit-backdrop-filter: blur(12px);
}

[data-testid="stSidebar"] {
   background: rgba(29, 35, 51, 0.95);
   backdrop-filter: blur(12px);
   -webkit-backdrop-filter: blur(12px);
}

.stSpinner > div > div {
   border-color: #3B82F6 #3B82F6 transparent !important;
}

.multiselect {
   background: rgba(55, 65, 81, 0.7);
   color: #F5F8FA;
   border: 1px solid rgba(255, 255, 255, 0.1);
   border-radius: 6px;
   backdrop-filter: blur(12px);
   -webkit-backdrop-filter: blur(12px);
}

@keyframes messageAppear {
   from { opacity: 0; transform: translateY(10px); }
   to { opacity: 1; transform: translateY(0); }
}

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
