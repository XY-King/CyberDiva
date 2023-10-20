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
    prompt = f"""I am now writing a story about the relationship and daily conversation between two imaginary characters.

The main character is as follows.
Character name: {charaSet["name"]}
Character settings: {charaSet["introduction"]}
{chara_settings}

The second imaginary character is as follows:
Character name: {userSet["name"]}
Character setting: {userSet["setting"]}

The current progress of writing the scripts of the story is as follows:

Here is the conversation history:
{combined_history}

Then, this is what happens:
{history[-1]['content']}

To help me write the scripts of the story, you should output three fields that would be considered when writing the response of {charaSet["name"]}: Communication, Action, and Thought. 
1. Communication: List all the detailed information that the character will express in the dialogue.
2. Action: Summarize the character's physical activities.
3. Thought: Summarize the character's internal emotional state and thoughts.

You should now output the information for the three fields {charaSet["name"]} would come up with in response to this. Only output the contents in the fields.
"""

    return {"role": "user", "content": prompt}


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
    result = f"""Here is the writing process of a story about a daily conversation between {charaSet['name']} and {userSet['name']}, as follows.
In the story, there are two imaginary characters.
    
The main character is {charaSet['name']}.
Character setting of {charaSet['name']}:
{intro}
{chara_settings}

The second character is {userSet['name']}.
Character setting of {userSet['name']}:
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

Finally, here is how Rinko would express the information in Rinko's tone and way of speaking, and play the corresponding motions in the scripts:
{charaSet['name']}: 
"""

    return result
