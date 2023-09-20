import openai
import os
import json
from sentence_transformers import SentenceTransformer

# run configuration
print("sentence transformer loading...")
model_embed = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(sentence: str):
    return model_embed.encode(sentence).tolist()

def get_embeddings(sentences: list[str]):
    embeddings = model_embed.encode(sentences)
    return [embedding.tolist() for embedding in embeddings]

def set_api_key():
    if os.path.exists("my_key.json"):
        key_id = "my_key.json"
    else:
        key_id = "key.json"

    api_key_setting = json.load(open(key_id, "rb"))

    key_id = api_key_setting["API_KEY_ID"]
    key = api_key_setting["API_KEYS"][key_id]

    openai.api_key = key["API_KEY"]
    if "API_TYPE" in key:
        openai.api_type = key["API_TYPE"]

