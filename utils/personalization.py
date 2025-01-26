import streamlit as st

def get_user_preferences():
    """Get user preferences from session state or default values."""
    if "preferences" not in st.session_state:
        st.session_state.preferences = {
            "favorite_memes": [],
            "favorite_topics": [],
            "enable_notifications": False,
            "user_name": "",
            "profile_pic": None,
            "interaction_history": []
        }
    return st.session_state.preferences

def update_preferences(favorite_memes=None, favorite_topics=None, enable_notifications=False, user_name="", profile_pic=None):
    """Update user preferences."""
    preferences = get_user_preferences()
    if favorite_memes is not None:
        preferences["favorite_memes"] = favorite_memes
    if favorite_topics is not None:
        preferences["favorite_topics"] = favorite_topics
    if enable_notifications is not None:
        preferences["enable_notifications"] = enable_notifications
    if user_name:
        preferences["user_name"] = user_name
    if profile_pic:
        preferences["profile_pic"] = profile_pic
    st.session_state.preferences = preferences

def add_interaction(query, response):
    """Add user interaction to history."""
    preferences = get_user_preferences()
    preferences["interaction_history"].append({"query": query, "response": response})
    st.session_state.preferences = preferences
