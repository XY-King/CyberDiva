import json
import openai
import os
from config import get_embeddings, get_embedding


def get_chara_setting_keys(charaSet: dict):
    keys = []
    for key in charaSet.keys():
        if type(charaSet[key]) is list:
            keys.append(key)
    return keys


def get_chara_config():
    # get character setting
    name = json.load(open("json/chara.json", "rb"))["name"]

    charaSet = json.load(open(f"characters/{name}/model.json", "rb"))
    charaSet = embed_chara(charaSet)
    # get live2d setting
    live2d = json.load(open(f"characters/{name}/live2d/model.json", "rb"))
    live2d_motions = list(live2d["motions"].keys())
    charaSet["motions"] = embed_live2d_motions(live2d_motions)
    # copy the live2d directory under the character to the static directory
    os.system("rm -rf static/live2d")
    os.system(f"cp -r characters/{name}/live2d static/live2d")
    # get examples setting
    with open(f"characters/{name}/examples.json", "rb") as f:
        examples = json.load(f)
    charaSet["examples"] = examples
    return charaSet


# make the sayings of the character into embeddings
def embed_chara(charaSet: dict):
    print("embedding character data...")
    # get all the keys where the value is a list but not a string
    keys = get_chara_setting_keys(charaSet)
    charaSet["setting_keys"] = keys

    # get the embeddings for the values of the keys
    for key in keys:
        values = charaSet[key]
        embeddings = get_embeddings(values)
        charaSet[key] = {"content": values, "embedding": embeddings}
    print("character data embedded")
    return charaSet


def embed_live2d_motions(motions: list[str]):
    print("embedding live2d motions...")
    # embed the motions
    motion_embeddings = get_embeddings(motions)
    # make the json file of the motions with the embeddings
    motions_embedded = {"content": motions, "embedding": motion_embeddings}
    print("live2d motions embedded")
    return motions_embedded


def get_user_config(chara_name: str):
    if os.path.exists("json/my_user.json"):
        id = "json/my_user.json"
    else:
        id = "json/user.json"

    userInit = json.load(open(id, "rb"))
    setting = userInit["setting"]
    setting = setting.replace("CHARACTER", chara_name)
    userInit["setting"] = setting
    return userInit
