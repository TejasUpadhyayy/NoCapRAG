import streamlit as st
from utils.api_utils import fetch_reddit_memes, fetch_giphy_gif, fetch_wikipedia_summary
from utils.gemini_utils import generate_response
from utils.chat_utils import initialize_chat_session, add_user_message, add_assistant_message, get_chat_context
from utils.personalization import get_user_preferences, update_preferences, add_interaction
from utils.trend_prediction import TrendPredictor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize trend predictor
if "trend_predictor" not in st.session_state:
    st.session_state.trend_predictor = TrendPredictor()

# Streamlit app
st.title("MemeMind: The Real-Time Meme Oracle 🧠🎭")
st.write("Ask me anything, and I'll answer with memes and Gen Z wisdom!")

# Sidebar for user preferences
with st.sidebar:
    st.header("Preferences")
    favorite_memes = st.multiselect("Favorite Memes", ["Dog Memes", "Cat Memes", "Relatable Memes", "Pop Culture"])
    favorite_topics = st.multiselect("Favorite Topics", ["Memes", "Pop Culture", "Trends", "Humor"])
    if st.button("Save Preferences"):
        update_preferences(favorite_memes, favorite_topics)

# Initialize chat session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = initialize_chat_session()

# Display chat messages
for message in st.session_state.chat_history:
    if message["role"] != "system":  # Don't display system messages
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "image" in message:
                st.image(message["image"])

# User input
if user_query := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.chat_history = add_user_message(st.session_state.chat_history, user_query)
    with st.chat_message("user"):
        st.write(user_query)

    # Step 1: Fetch relevant memes and pop culture references
    memes = fetch_reddit_memes(limit=3)
    gif_url = fetch_giphy_gif(user_query)
    wiki_summary = fetch_wikipedia_summary(user_query)

    # Step 2: Generate response using Gemini
    context = (
        "You are MemeMind, a friendly and relatable chatbot that uses memes and humor to make conversations fun. "
        "Keep your tone conversational, empathetic, and lighthearted. Avoid over-the-top enthusiasm or dark humor.\n\n"
        "Context:\n"
    )
    context += get_chat_context(st.session_state.chat_history)
    if wiki_summary:
        context += f"\n\nWikipedia: {wiki_summary}"
    response = generate_response(user_query, context)

    # Step 3: Display response
    st.session_state.chat_history = add_assistant_message(st.session_state.chat_history, response, gif_url)
    with st.chat_message("assistant"):
        st.write(response)
        if gif_url:
            st.image(gif_url)

    # Step 4: Update interaction history
    add_interaction(user_query, response)

    # Step 5: Update trend data
    for meme in memes:
        st.session_state.trend_predictor.add_data(meme["title"])

# Display trend predictions
trends = st.session_state.trend_predictor.predict_trends()
if trends:
    st.write("### Trending Memes:")
    for trend in trends:
        st.write(f"- {trend}")
