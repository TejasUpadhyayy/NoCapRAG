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
st.title("NoCap RAG ")
st.write("Ask me anything, and I'll answer with memes and Gen Z wisdom!")

# Sidebar for user preferences
# Sidebar for user preferences
with st.sidebar:
    st.header("Preferences")

    # Theme Selector
    theme = st.selectbox("Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Favorite Memes
    st.subheader("Favorite Memes")
    favorite_memes = st.multiselect(
        "Choose your favorite memes",
        ["Dog Memes", "Cat Memes", "Relatable Memes", "Tech Memes", "Gaming Memes"]
    )

    # Favorite Topics
    st.subheader("Favorite Topics")
    favorite_topics = st.multiselect(
        "Choose your favorite topics",
        ["Memes", "Pop Culture", "Trends", "Humor", "Tech", "Gaming"]
    )

    # Trend Notifications
    st.subheader("Notifications")
    enable_notifications = st.checkbox("Notify me about trending memes")

    # User Name
    st.subheader("Profile")
    user_name = st.text_input("Enter your name")

    # Save Preferences
    if st.button("Save Preferences"):
        update_preferences(
            favorite_memes=favorite_memes,
            favorite_topics=favorite_topics,
            enable_notifications=enable_notifications,
            user_name=user_name
        )
        st.success("Preferences saved!")
        
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
        "You are NoCap, a chatbot who’s just trying to keep things chill while vibing with the conversation. "
        "You use memes, jokes, and the kind of humor that hits right where it’s supposed to—nothing forced, just genuine laughs. "
        "You’re here to make things lighter and more fun, but also to listen and keep it real. We’re not about drama or fake energy; you’re the one that gets how it feels to be in the moment—no cap.\n\n"
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
