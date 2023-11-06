from config import get_embedding
from copy import deepcopy
import locale
from sentence_transformers import util
import numpy as np


# filter the sayings by the relation with the input and return the top {num} sayings
def filter_sayings(
    sayings: list, embeddings: list, input: str, num: int, is_stable: bool = False
):
    input_embedding = get_embedding(input)
    cos_sim = util.cos_sim(input_embedding, np.array(embeddings))[0]
    pairs = []
    for i, saying in enumerate(sayings):
        pairs.append({"index": i, "relation": cos_sim[i]})

    # sort the sayings by the relation from the highest to the lowest
    pairs.sort(key=lambda x: x["relation"], reverse=True)
    # get the first {num} sayings
    pairs = pairs[:num]
    # output the result into a list
    result_sayings = []
    for pair in pairs:
        result_sayings.append(sayings[pair["index"]])
    
    return result_sayings


# filter the history, the filter result musty have pairs of user and assistant
def filter_history(history: list, history_embeddings: list, input: str, num: int):
    # add index to the history
    history_copy = deepcopy(history)
    for i in range(len(history_copy)):
        history_copy[i]["index"] = i
    filtered_history = filter_sayings(
        sayings=history_copy,
        embeddings=history_embeddings,
        input=input,
        num=num,
        is_stable=True,
    )
    result = []
    for msg in filtered_history:
        if msg["role"] == "user":
            result.append(history_copy[msg["index"]])
            if msg["index"] < len(history_copy) - 1:
                if not history_copy[msg["index"] + 1] in filtered_history:
                    result.append(history_copy[msg["index"] + 1])
        else:
            if not history_copy[msg["index"] - 1] in filtered_history:
                result.append(history_copy[msg["index"] - 1])
            result.append(history_copy[msg["index"]])
    for msg in result:
        msg.pop("index")
    return result


# combine a list of sayings with embeddings into one string
def combine_sayings(sayings: list, with_quotation=True):
    result = ""
    for i, saying in enumerate(sayings):
        if with_quotation:
            if i == len(sayings) - 1:
                result += f"\"{saying}\""
            else:
                result += f"\"{saying}\"\n"
        else:
            if i == len(sayings) - 1:
                result += f"{saying}"
            else:
                result += f"{saying}\n"
    result = result.rstrip("\n")
    return result


def change_language():
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
