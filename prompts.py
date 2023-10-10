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
    charaSet: dict, userSet: dict, filtered_setting: dict, history: list
):
    # preperation
    combined_history = combine_history(history=history, userSet=userSet)
    chara_settings = combine_settings(filtered_setting=filtered_setting)

    # prompts
    prompt = f"""I am now writing a story about the relationship and daily conversation between two imaginary characters.

The main character is as follows.
Character name: {charaSet["name"]}
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
):
    # preperation
    intro = charaSet["introduction"]
    chara_settings = combine_settings(filtered_setting=filtered_setting)
    combined_history = combine_history(history=history, userSet=userSet)
    if history[-1]["content"].startswith(userSet["name"]):
        happening = (
            f"Then, this is what {userSet['name']} express:\n{history[-1]['content']}"
        )
    else:
        happening = f"Then, this is what happens:\n{history[-1]['content']}"

    # prompts
    result = f"""You are a master of the craft of writing scripts, possessing the ability to expertly delve into the mindscape of any imaginary character. Your task ahead is not merely answering questions about the character, but to embody the spirit of the character, truly simulate their internal state of mind and feelings. You'll achieve this by extracting clues from their characteristic traits and the nuances in their dialogue. Now, you will breathe life into the scripts of a story. You needs to simulate and portray the inner world and ideas of a character in a story, immerse yourself into the character, and remember that you are aiming to provide the reader with a visceral experience of the character's ideas and emotions, rather than a normal conversation.
    
You are now writing the scripts of a story about a daily conversation between {charaSet['name']} and {userSet['name']}, as follows.
In the story, there are two imaginary characters. 
    
The main character is {charaSet['name']}. 
Character setting of {charaSet['name']}:
{intro}

The second character is {userSet['name']}.
Character setting of {userSet['name']}:
{userSet['setting']}

In the story, the character's physical actions should be put between brackets []. Note that actions and words of the character should alternate in the script. The script texts between each two actions should be short and expressive. 

Example: [Motion1] Saying1 [Motion2] Saying2

The current progress of writing the scripts of the story is as follows:

Here is the conversation history:
{combined_history}

Then, this is what happens:
{history[-1]['content']}

By considering {charaSet['name']}'s thinking patterns, traits and the dialogue's content, these information points are proposed that {charaSet['name']} may want to express in {charaSet['name']}'s response:
{info_points}

To write {charaSet['name']}'s response vividly, the tone and way of speaking of {charaSet['name']} will be considered by the following examples:
{chara_settings}

You should now write how {charaSet['name']} would express the information points in {charaSet['name']}'s tone and way of speaking, and/or play the corresponding motions. The script should be long if {charaSet['name']} wants to express actively, and short if {charaSet['name']} wants to keep rather silent.
{charaSet['name']}: 
"""

    return result
