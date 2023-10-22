import string
from openai.embeddings_utils import cosine_similarity
from config import get_embedding, get_embeddings
from utils import filter_sayings, filter_history, combine_sayings
from copy import deepcopy


# HELPER FUNCTIONS
def combine_settings(filtered_setting: dict):
    chara_settings = ""
    for key in filtered_setting.keys():
        chara_settings += f"Character {key}:\n{filtered_setting[key]}\n\n"
    return chara_settings


def combine_history(history: list, userSet: dict):
    history_copy = deepcopy(history)
    history_copy.pop()
    filtered_history = filter_history(
        history=history_copy,
        input=history[-1]["content"],
        num=20,
    )
    if filtered_history == []:
        done_history = "There is no history yet."
    else:
        done_history = combine_sayings(filtered_history, with_quotation=False)

    return done_history


# PROMPTS FUNCTIONS


def get_intro_prompts(
    charaSet: dict,
    userSet: dict,
    filtered_setting: dict,
    history: list,
    is_stable: bool = True,
):
    # preperation
    combined_history = combine_history(history=history, userSet=userSet)
    if is_stable:
        chara_settings = ""
    else:
        chara_settings = combine_settings(filtered_setting=filtered_setting)

    # prompts
    prompt = f"""Here is the writing process of a story about a daily conversation between {charaSet['name']} and {userSet['name']}.
In the story, there are two imaginary characters.

The main character is {charaSet["name"]}.
Character setting: 
{charaSet["introduction"]}
{chara_settings}

The second imaginary character is {userSet["name"]}.
Character setting: 
{userSet["setting"]}

The current progress of writing the scripts of the story is as follows:

Here is the conversation history:
{combined_history}

There are two steps to continue writing the scripts.
The first step is to consider three fields in the response of Rinko: ACTION, THOUGHT, and COMMUNICATION. 
THOUGHT: A summary of the {charaSet["name"]}'s internal emotional state and thoughts.
ACTION: A summary of the {charaSet["name"]}'s physical activities. Focus on the body movements and facial expressions.
COMMUNICATION: An outline of points that {charaSet["name"]} will convey in the dialogue. Only information points but not the exact words.

Examples:
THOUGHT: {charaSet["name"]} would feel (...).
ACTION: {charaSet["name"]} would raise (...).
COMMUNICATION: {charaSet["name"]} would mention (...). {charaSet["name"]} would also inquire (...).

By considering the Rinko's personality and the current scene, here is the fields contents in Rinko's performance in response to this:
{history[-1]['content']}"""

    return prompt


def get_tone_prompts(
    charaSet: dict,
    userSet: dict,
    history: list,
    info_points: string,
    filtered_setting: dict,
    is_stable: bool = True,
):
    # preperation
    intro = charaSet["introduction"]
    if is_stable:
        chara_settings = ""
    else:
        chara_settings = combine_settings(filtered_setting=filtered_setting)
    combined_history = combine_history(history=history, userSet=userSet)

    # prompts
    result = f"""Here is the writing process of a story about a daily conversation between {charaSet['name']} and {userSet['name']}.
In the story, there are two imaginary characters.
    
The main character is {charaSet['name']}.
Character setting:
{intro}
{chara_settings}

The second character is {userSet['name']}.
Character setting:
{userSet['setting']}

The current progress of writing the scripts of the story is as follows:
Here is the conversation history:
{combined_history}

Then, this is what happens:
{history[-1]['content']}

By considering {charaSet['name']}'s thinking patterns, traits and the dialogue's content, these information are considered possible in {charaSet['name']}'s response:
{info_points}

In the story, the character's physical actions should be put between brackets []. Note that actions and words of the character should alternate in the script. The script texts between each two actions should be short and expressive. 
Example: [Motion] Words [Motion] Words

Finally, here is how Rinko would express the information in {charaSet["name"]}'s tone and way of speaking, and play the corresponding motions in the scripts:
{charaSet['name']}:"""

    return result
