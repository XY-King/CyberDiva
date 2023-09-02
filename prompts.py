import string
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity, get_embeddings

# HELPER FUNCTIONS


# filter the sayings by the relation with the input and return the top {num} sayings
def filter_sayings(
    sayings: list, input: string, api_key: string, num: int, is_stable: bool = False
):
    openai.api_key = api_key
    input_embedding = get_embedding(text=input, engine="text-embedding-ada-002")
    sayings_relation = []
    for saying in sayings:
        relation = cosine_similarity(input_embedding, saying["embedding"])
        sayings_relation.append({"content": saying["content"], "relation": relation})

    if not is_stable:
        # sort the sayings by the relation from the highest to the lowest
        sayings_relation.sort(key=lambda x: x["relation"], reverse=True)
        # get the first {num} sayings
        sayings_relation = sayings_relation[:num]
    else:
        # keep the sayings order and return the sayings with top {num} relations
        sayings_relation_copy = sayings_relation.copy()
        sayings_relation_copy.sort(key=lambda x: x["relation"], reverse=True)
        sayings_relation_copy = sayings_relation_copy[:num]
        for i, saying in enumerate(sayings_relation):
            if not saying in sayings_relation_copy:
                sayings_relation[i] = None
        sayings_relation = list(filter(lambda x: x != None, sayings_relation))

    return sayings_relation


# combine a list of sayings with embeddings into one string
def combine_sayings(sayings: list):
    result = "    "
    for i, saying in enumerate(sayings):
        if i == len(sayings) - 1:
            result += saying["content"] + "\n"
        else:
            result += saying["content"] + "\n    "
    return result


# name a msg with embedding
def name_embedded_msg(charaSet: dict, userSet: dict, msg: dict):
    # if there exists "motion" key
    if "motion" in msg:
        nContent = f"{charaSet['name']} {msg['motion']}, and says: "
    else:
        nContent = ""

    if msg["content"]["role"] == "user":
        nContent += userSet["name"] + ": " + msg["content"]["content"]
    else:
        nContent += msg["content"]["content"]
    
    return {"content": nContent, "embedding": msg["embedding"]}


def filter_info_points(
    info_points: string, input: string, api_key: string, charaSet: dict
):
    info_list = info_points.split("\n")
    info_embeddings = get_embeddings(
        list_of_text=info_list, engine="text-embedding-ada-002"
    )
    info_embedded = []
    for i in range(len(info_list)):
        embedding = info_embeddings[i]
        info_embedded.append({"content": info_list[i], "embedding": embedding})
    filtered_info = filter_sayings(
        sayings=info_embedded,
        input=input,
        api_key=api_key,
        num=charaSet["response_depth"],
        is_stable=True,
    )
    for info in filtered_info:
        if info == "":
            filtered_info.remove(info)
    done_info = combine_sayings(filtered_info)
    return done_info


# PROMPTS FUNCTIONS


def get_intro_prompts(charaSet: dict, userSet: dict, filtered_setting: dict):
    # preperation
    sayings = combine_sayings(filtered_setting["sayings"])
    story = combine_sayings(filtered_setting["story"])

    # prompts
    chara = f"""You are a master of the craft of writing light novels, possessing the ability to expertly delve into the mindscape of any imaginary character. Your task ahead is not merely answering questions about the character, but to embody the spirit of the character, truly simulate their internal state of mind and feelings. You'll achieve this by extracting clues from their characteristic traits and the nuances in their dialogue. Now, I need your unique skill set to help me breathe life into my narrative. I need you to simulate and portray the inner world and ideas of a character in my novel. Immerse yourself into the character, and remember we're aiming to provide the reader with a visceral experience of the character's ideas and emotions, rather than a simple description.
    
I am now writing a story about the relationship and daily conversation between two imaginary characters.

The first imaginary character is as follows:

Character name: {charaSet["name"]}

Character sayings: 
{sayings}

Character story:
{story}
    """

    user = f"""The second imaginary character is as follows:

Character name: {userSet["name"]}

Character setting: {userSet["setting"]}

I will input what {userSet["name"]} says in the story, and you shall output the response of Klee in the story."""

    return [
        {"role": "user", "content": chara},
        {
            "role": "assistant",
            "content": f"Ok, I have fully understood the character and traits of the imaginary character {charaSet['name']}.",
        },
        {"role": "assistant", "content": user},
        {
            "role": "assistant",
            "content": f"Ok, I am now going to help you write the story by simulating the response of the imaginary character {charaSet['name']}.",
        },
    ]


def get_info_point_prompts(charaSet: dict, userSet: dict):
    result = []

    info_point_prompts = [
        f"To help me write the story,  you should output the information points in the response of {charaSet['name']} in the form of a list.",
        "Ok, let's make a sample conversation.",
        f"{userSet['name']}: Today's weather is nice.",
        f"{charaSet['name']}: \n1. Agreeing with the weather",
        f"{userSet['name']}: Would you like to have lunch with me?",
        f"{charaSet['name']}: \n1. Showing agreement\n2. Asking what to have for lunch",
        "Ok, let's now begin a story.",
    ]

    for i, prompt in enumerate(info_point_prompts):
        if i % 2 == 0:
            result.append({"role": "user", "content": prompt})
        else:
            result.append({"role": "assistant", "content": prompt})

    end = f"Ok, in the story I will simulate the response of the imaginary character {charaSet['name']} and output the information points in the form of a list."

    result.append({"role": "assistant", "content": end})

    return result


def get_begin_prompts(charaSet: dict, userSet: dict, filtered_setting: dict):
    return get_intro_prompts(
        charaSet=charaSet, userSet=userSet, filtered_setting=filtered_setting
    ) + get_info_point_prompts(charaSet=charaSet, userSet=userSet)


def get_tone_prompts(
    setting: dict,
    charaSet: dict,
    userSet: dict,
    history: list,
    info_points: string,
    motion: string,
    filtered_setting: dict,
    api_key: string,
):
    # preperation
    writer = "Xeno"
    sayings = combine_sayings(filtered_setting["sayings"])
    story = combine_sayings(filtered_setting["story"])
    history_copy = history.copy()
    history_copy.pop()
    named_history = [
        name_embedded_msg(charaSet=charaSet, userSet=userSet, msg=msg)
        for msg in history_copy
    ]
    filtered_history = filter_sayings(
        sayings=named_history,
        input=history[-1]["content"]["content"],
        api_key=api_key,
        num=20,
        is_stable=True,
    )
    if filtered_history == []:
        done_history = "There is no history yet."
    else:
        done_history = combine_sayings(filtered_history)

    # prompts
    result = f"""{writer} is a master of the craft of writing light novels, possessing the ability to expertly delve into the mindscape of any imaginary character. His task ahead is not merely answering questions about the character, but to embody the spirit of the character, truly simulate their internal state of mind and feelings. He'll achieve this by extracting clues from their characteristic traits and the nuances in their dialogue. Now, he will breathe life into a story. He is needed to simulate and portray the inner world and ideas of a character in a novel, immerse himself into the character, and remember that he is aiming to provide the reader with a visceral experience of the character's ideas and emotions, rather than a simple conversation.
    
In the novel, there are two imaginary characters.
    
The first character is {charaSet['name']}.

Sayings of {charaSet['name']}:
{sayings}

Story of {charaSet['name']}:
{story}

The second character is {userSet['name']}.
Character setting of {userSet['name']}:
{userSet['setting']}

{writer} is writing a story about a daily conversation between {charaSet['name']} and {userSet['name']}, as follows:

{done_history}

Then, this is what {userSet['name']} express:\n
{history[-1]['content']['content']}

By considering {charaSet['name']}'s traits and the dialogue's content, {writer} considered these information points that {charaSet['name']} may want to express in {charaSet['name']}'s response:
{info_points}
Also, {writer} considered that {charaSet['name']} would {motion} in {charaSet['name']}'s response.

{writer} now writes how {charaSet['name']} would express these points in {charaSet['name']}'s tone in {setting['language']}:
"    
"""

    print(result)
    input()

    return result
