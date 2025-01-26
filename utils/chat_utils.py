def initialize_chat_session():
    """Initialize the chat session with a system message."""
    return [{"role": "system", "content": "You are MemeMind, a witty and meme-savvy assistant. Respond with humor and Gen Z vibes."}]

def add_user_message(chat_history, user_query):
    """Add a user message to the chat history."""
    chat_history.append({"role": "user", "content": user_query})
    return chat_history

def add_assistant_message(chat_history, response, image_url=None):
    """Add an assistant message to the chat history."""
    message = {"role": "assistant", "content": response}
    if image_url:
        message["image"] = image_url
    chat_history.append(message)
    return chat_history

def get_chat_context(chat_history):
    """Extract the conversation context from the chat history."""
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])