import string
from openai.embeddings_utils import cosine_similarity
from config import get_embedding, get_embeddings
from utils import filter_sayings, filter_history, combine_sayings
from copy import deepcopy
from datetime import datetime


# HELPER FUNCTIONS
def combine_settings(filtered_setting: dict):
    chara_settings = ""
    for key in filtered_setting.keys():
        chara_settings += f"Character {key}:\n{filtered_setting[key]}\n\n"
    return chara_settings


def combine_history(history: list, userSet: dict):
    history_copy = deepcopy(history)
    filtered_history = filter_history(
        history=history_copy,
        input=history[-1]["content"],
        num=100,
    )
    done_history = combine_sayings(filtered_history, with_quotation=False)

    return done_history


# PROMPTS FUNCTIONS


def get_fields_prompt(
    charaSet: dict,
    userSet: dict,
    filtered_setting: dict,
    history: list,
    is_stable: bool = True,
):
    # preperation
    combined_history = combine_history(history=history, userSet=userSet)

    # prompts
    prompt = f"""```MAIN CHARACTER
Character name: {charaSet['name']}
Character setting: 
{charaSet["introduction"]}
```

```SECOND CHARACTER
Character name: {userSet["name"]}
Character setting: 
{userSet["setting"]} 
```

```REQUIREMENTS
Consider two fields in the response of {charaSet["name"]}: THOUGHT and ACTION, by taking {charaSet["name"]}'s personality and current scene into account.
THOUGHT: A summary of the {charaSet["name"]}'s internal emotional state and thoughts.
ACTION: A summary of the {charaSet["name"]}'s physical activities. Focus on the body movements and facial expressions.

Example:
LONG 
I like your costume today, it's cute

RINKO
THOUGHT: Rinko is surprised by Long's comment. She would feel a mix of happiness and embarrassment at the compliment. She would be eager to show that this is the clothes for Roseilia's next live.
ACTION: Rinko would blush, fidget nervously with her hands, and glance down at her outfit.
```

```HISTORY
{combined_history}
```

```{charaSet["name"].upper()}
"""

    return prompt


def get_script_prompt(
    charaSet: dict,
    userSet: dict,
    history: list,
    fields: string,
    filtered_setting: dict,
    is_stable: bool = True,
):
    # preperation
    combined_history = combine_history(history=history, userSet=userSet)
    timing = datetime.now().strftime("%Y/%m/%d %H:%M")

    # prompts
    result = f"""```MAIN CHARACTER
Character name: {charaSet['name']}
Character setting: 
{charaSet["introduction"]}
```

```SECOND CHARACTER
Character name: {userSet["name"]}
Character setting: 
{userSet["setting"]} 
```

```REQUIREMENTS
Consider {charaSet['name']}'s next performance in response to what just happened, in {charaSet['name']}'s tone and personality.
In the story, {charaSet['name']}'s physical actions should be put between brackets []. Actions and words of {charaSet['name']} should appear alternately. 
Example: [Motion] Words [Motion] Words
```

```HISTORY
{combined_history}
```

```{charaSet["name"].upper()}
{fields}
PERFORMANCE: {timing} {charaSet["name"]}:"""

    return result
