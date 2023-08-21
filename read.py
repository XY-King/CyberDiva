import json
import string
import openai

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
    saying_embeddings = openai.Embedding.create(
                        model="text-embedding-ada-002",
                        input=charaInit["sayings"]
                    )
    saying_embeddings = saying_embeddings["data"]
    story_embeddings = openai.Embedding.create(
                        model="text-embedding-ada-002",
                        input=charaInit["story"]
                    )
    story_embeddings = story_embeddings["data"]
    
    sayings_embedded = []
    for i in range(len(charaInit["sayings"])):
        embedding = saying_embeddings[i]["embedding"]
        sayings_embedded.append({"content": charaInit["sayings"][i], "embedding": embedding})
    
    story_embedded = []
    for i in range(len(charaInit["story"])):
        embedding = story_embeddings[i]["embedding"]
        story_embedded.append({"content": charaInit["story"][i], "embedding": embedding})

    charaInit["is_embedded"] = True
    with open(f"characters/{name}.json", "w", encoding="UTF-8") as f:
        json.dump(charaInit, f, ensure_ascii=False, indent=4)
    charaInit["sayings"] = sayings_embedded
    charaInit["story"] = story_embedded
    with open(f"characters/{name}_embedded.json", "w", encoding="UTF-8") as f:
        json.dump(charaInit, f, ensure_ascii=False, indent=4)
