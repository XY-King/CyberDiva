import json
import string
import openai
import os
from openai.embeddings_utils import get_embeddings, get_embedding


def get_chara_config(api_key: string):
    # get character setting
    name = json.load(open("chara.json", "rb"))["name"]
    is_embedded = json.load(open(f"characters/{name}.json", "rb"))["is_embedded"]

    if not is_embedded:
        embed_chara(name, api_key)

    charaSet = json.load(open(f"characters/{name}_embedded.json", "rb"))

    # get live2d setting
    live2d_name = json.load(open("chara.json", "rb"))["live2d"]
    embed_live2d_motions(live2d_name, api_key)
    with open(f"live2d/{live2d_name}/motions_embedded.json", "rb") as f:
        live2d_motions = json.load(f)
    charaSet["motions"] = live2d_motions
    return charaSet


# make the sayings of the character into embeddings
def embed_chara(name: string, api_key: string):
    charaInit = json.load(open(f"characters/{name}.json", "rb"))
    openai.api_key = api_key

    # get the embeddings for the sayings and the story
    saying_embeddings = get_embeddings(
        list_of_text=charaInit["sayings"], engine="text-embedding-ada-002"
    )
    story_embeddings = get_embeddings(
        list_of_text=charaInit["story"], engine="text-embedding-ada-002"
    )

    # make the json file of the character with the embeddings
    sayings_embedded = []
    for i in range(len(charaInit["sayings"])):
        embedding = saying_embeddings[i]
        sayings_embedded.append(
            {"content": charaInit["sayings"][i], "embedding": embedding}
        )

    story_embedded = []
    for i in range(len(charaInit["story"])):
        embedding = story_embeddings[i]
        story_embedded.append(
            {"content": charaInit["story"][i], "embedding": embedding}
        )

    # change the "is_embedded" to True
    charaInit["is_embedded"] = True
    with open(f"characters/{name}.json", "w", encoding="UTF-8") as f:
        json.dump(charaInit, f, ensure_ascii=False, indent=4)
    # output the json file with embeddings
    charaInit["sayings"] = sayings_embedded
    charaInit["story"] = story_embedded
    with open(f"characters/{name}_embedded.json", "w", encoding="UTF-8") as f:
        json.dump(charaInit, f, ensure_ascii=False, indent=4)


def embed_live2d_motions(live2d_name: string, api_key: string):
    # if the motions_embedded.json file exists, then return
    if os.path.exists(f"live2d/{live2d_name}/motions_embedded.json"):
        return

    # get the motions
    live2d_model = json.load(open(f"live2d/{live2d_name}/model.json", "rb"))
    live2d_motions = live2d_model["motions"]
    # get all the keys of the motions and transform it into a list
    live2d_motions = list(live2d_motions.keys())

    # embed the motions
    openai.api_key = api_key
    motion_embeddings = get_embeddings(
        list_of_text=live2d_motions, engine="text-embedding-ada-002"
    )
    # make the json file of the motions with the embeddings
    motions_embedded = []
    for i in range(len(live2d_motions)): 
        embedding = motion_embeddings[i]
        motions_embedded.append(
            {"content": live2d_motions[i], "embedding": embedding}
        )
    # output the json file with embeddings
    with open(f"live2d/{live2d_name}/motions_embedded.json", "w", encoding="UTF-8") as f:
        json.dump(motions_embedded, f, ensure_ascii=False, indent=4)
