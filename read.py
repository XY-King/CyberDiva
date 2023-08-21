import json
import string
import openai
from openai.embeddings_utils import get_embeddings

def get_chara_config(api_key: string):
    name = json.load(open("chara.json", "rb"))["name"]
    is_embedded = json.load(open(f"characters/{name}.json", "rb"))["is_embedded"]

    if not is_embedded:
        embed_chara(name, api_key)

    charaSet = json.load(open(f"characters/{name}_embedded.json", "rb"))
    return charaSet

# make the sayings of the character into embeddings
def embed_chara(name: string, api_key: string):
    charaInit = json.load(open(f"characters/{name}.json", "rb"))
    openai.api_key = api_key

    # get the embeddings for the sayings and the story
    saying_embeddings = get_embeddings(list_of_text=charaInit["sayings"], engine="text-embedding-ada-002")
    story_embeddings = get_embeddings(list_of_text=charaInit["story"], engine="text-embedding-ada-002")
    
    # make the json file of the character with the embeddings
    sayings_embedded = []
    for i in range(len(charaInit["sayings"])):
        embedding = saying_embeddings[i]
        sayings_embedded.append({"content": charaInit["sayings"][i], "embedding": embedding})
    
    story_embedded = []
    for i in range(len(charaInit["story"])):
        embedding = story_embeddings[i]
        story_embedded.append({"content": charaInit["story"][i], "embedding": embedding})

    # change the "is_embedded" to True
    charaInit["is_embedded"] = True
    with open(f"characters/{name}.json", "w", encoding="UTF-8") as f:
        json.dump(charaInit, f, ensure_ascii=False, indent=4)
    # output the json file with embeddings
    charaInit["sayings"] = sayings_embedded
    charaInit["story"] = story_embedded
    with open(f"characters/{name}_embedded.json", "w", encoding="UTF-8") as f:
        json.dump(charaInit, f, ensure_ascii=False, indent=4)
