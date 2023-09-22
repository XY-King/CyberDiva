from config import get_embedding
from openai.embeddings_utils import cosine_similarity
from copy import deepcopy

def with_embedding(msg: dict):
    msg_copy = deepcopy(msg)
    embedding = get_embedding(msg["content"])
    msg_copy["embedding"] = embedding
    return msg_copy

# filter the sayings by the relation with the input and return the top {num} sayings
def filter_sayings(sayings: list, input: str, num: int, is_stable: bool = False):
    sayings_copy = deepcopy(sayings)
    input_embedding = get_embedding(input)
    for saying in sayings_copy:
        relation = cosine_similarity(input_embedding, saying["embedding"])
        saying["relation"] = relation
        
    if not is_stable:
        # sort the sayings by the relation from the highest to the lowest
        sayings_copy.sort(key=lambda x: x["relation"], reverse=True)
        # get the first {num} sayings
        sayings_copy = sayings_copy[:num]
    else:
        # keep the sayings order and return the sayings with top {num} relations
        sayings_sorted = deepcopy(sayings_copy)
        sayings_sorted.sort(key=lambda x: x["relation"], reverse=True)
        sayings_sorted = sayings_sorted[:num]
        for i, saying in enumerate(sayings_copy):
            if not saying in sayings_sorted:
                sayings_copy[i] = None
        sayings_copy = list(filter(lambda x: x != None, sayings_copy))
    
    for saying in sayings_copy:
        saying.pop("relation")

    return sayings_copy

# filter the history, the filter result musty have pairs of user and assistant
def filter_history(history: list, input: str, num: int):
    # add index to the history
    history_copy = deepcopy(history)
    for i in range(len(history_copy)):
        history_copy[i]["index"] = i
    filtered_history = filter_sayings(
        sayings=history_copy,
        input=input,
        num=num,
        is_stable=True,
    )
    result = []
    for msg in filtered_history:
        if msg["role"] == "user":
            result.append(history[msg["index"]])
            if msg["index"] < len(history) - 1:
                if not history[msg["index"] + 1] in filtered_history:
                    result.append(history[msg["index"] + 1])
        else:
            if not history[msg["index"] - 1] in filtered_history:
                result.append(history[msg["index"] - 1])
            result.append(history[msg["index"]])

    return result

# combine a list of sayings with embeddings into one string
def combine_sayings(sayings: list, with_quotation=True):
    result = "    "
    for i, saying in enumerate(sayings):
        if with_quotation:
            if i == len(sayings) - 1:
                result += f"\"{saying['content']}\"\n"
            else:
                result += f"\"{saying['content']}\"\n    "
        else:
            if i == len(sayings) - 1:
                result += f"{saying['content']}\n"
            else:
                result += f"{saying['content']}\n    "
    return result