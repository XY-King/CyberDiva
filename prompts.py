import string
from utils import filter_history, combine_sayings
from copy import deepcopy


# HELPER FUNCTIONS
def combine_settings(filtered_setting: dict):
    chara_settings = ""
    for key in filtered_setting.keys():
        # upper the first letter of the key
        nKey = key.capitalize()
        chara_settings += f"{nKey}:\n{filtered_setting[key]}\n\n"
    chara_settings = chara_settings.rstrip("\n")
    return chara_settings


def combine_examples(
    chara: str, user: str, examples: list, include_performance: bool = False
):
    combined_examples = ""
    for i, example in enumerate(examples):
        combined_examples += f"__Example_{i+1}__:\n"
        combined_examples += user.upper() + "\n"
        combined_examples += example["message"] + "\n"
        combined_examples += chara.upper() + "\n"
        combined_examples += example["fields"] + "\n"
        if include_performance:
            combined_examples += f"PERFORMANCE: {example['performance']}\n"
    combined_examples = combined_examples.rstrip("\n")
    return combined_examples


def extract_msg(user: str, msg: str):
    if msg.startswith(user):
        id = user.upper()
        msg = msg[len(user) + 2 :]
    else:
        id = "HAPPENING"

    result = f"""{id}
{msg}"""
    return result


# PROMPTS FUNCTIONS


def get_fields_prompt(
    charaSet: dict,
    userSet: dict,
    filtered_setting: dict,
    history: list,
    is_stable: bool = True,
):
    # preperation
    if is_stable:
        settings = combine_settings(filtered_setting=filtered_setting)
    else:
        settings = ""
    examples = combine_examples(
        chara=charaSet["name"], user=userSet["name"], examples=charaSet["examples"]
    )
    combined_history = combine_sayings(sayings=history[:-1], with_quotation=False)
    last_msg = history[-1]
    last_msg = extract_msg(user=userSet["name"], msg=last_msg)

    # prompts
    prompt = f"""```REQUIREMENTS
Consider two fields in the performance of {charaSet["name"]}: THOUGHT and ACTION, by taking {charaSet["name"]}'s personality and current scene into account.
THOUGHT: A summary of the {charaSet["name"]}'s internal emotional state and thoughts.
ACTION: A summary of the {charaSet["name"]}'s physical activities. Focus on the body movements and facial expressions.
{examples}
```
    
```MAIN CHARACTER
Character name: {charaSet['name']}
Character setting: 
{charaSet["introduction"]}
```

```SECOND CHARACTER
Character name: {userSet["name"]}
Character setting: 
{userSet["setting"]} 
```

```SCENE
{combined_history}
```

```FOLLOWING
{last_msg}
{charaSet["name"].upper()}  
THOUGHT:
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
    settings = combine_settings(filtered_setting=filtered_setting)
    examples = combine_examples(
        chara=charaSet["name"],
        user=userSet["name"],
        examples=charaSet["examples"],
        include_performance=True,
    )
    combined_history = combine_sayings(sayings=history[:-1], with_quotation=False)
    last_msg = history[-1]
    last_msg = extract_msg(user=userSet["name"], msg=last_msg)

    # prompts
    result = f"""```REQUIREMENTS
Consider the following performance of {charaSet['name']}, by taking {charaSet["name"]}'s personality and current scene into account.
In the story, {charaSet['name']}'s physical actions should be put between brackets []. Actions and words of {charaSet['name']} should appear alternately. 
{examples}
```

```MAIN CHARACTER
Character name: {charaSet['name']}
Character setting: 
{charaSet["introduction"]}

{settings}
```

```SECOND CHARACTER
Character name: {userSet["name"]}
Character setting: 
{userSet["setting"]} 
```

```SCENE
{combined_history}
```

```FOLLOWING
{last_msg}
{charaSet["name"].upper()}
{fields}
PERFORMANCE:"""

    return result
