# chatbot.py
from config import model

def get_chatbot_response(user_message):
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]
    )
    response = chat.send_message(user_message)
    return response.text
