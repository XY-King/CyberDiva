from prompts import filter_history
from config import get_embedding

history = [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "hi"},
    {"role": "user", "content": "how are you?"},
    {"role": "assistant", "content": "I am an AI assistant programmed to provide support. How can I assist you today?"},
    {"role": "user", "content": "I need help with resetting my password"},
    {"role": "assistant", "content": "Sure thing! Can you provide me with your username so I can assist you better?"},
    {"role": "user", "content": "My username is johndoe123"},
    {"role": "assistant", "content": "Got it. One moment while I look into your account."},
    {"role": "assistant", "content": "I have sent a password reset link to your email. Please check and follow the instructions to reset your password."},
    {"role": "user", "content": "Thank you so much!"},
    {"role": "assistant", "content": "You're welcome. Is there anything else I can help you with?"},
    {"role": "user", "content": "No, that's all for now. Thanks again!"},
    {"role": "assistant", "content": "My pleasure. Have a great day!"}
]

for msg in history:
    msg["embedding"] = get_embedding(msg["content"])

filtered_history = filter_history(history=history, input="What is your name?", num = 4)
for msg in filtered_history:
    msg.pop("embedding")
print(filtered_history)
