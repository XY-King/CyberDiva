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

    # find the timing in the msg like 2023/11/03 09:54
    time = msg[:16]
    msg = msg[17:]

    result = f"""```{time} {id}
{msg}
```"""
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
    combined_history = combine_sayings(sayings=history, with_quotation=False)
    last_msg = history[-1]["content"]
    last_msg = extract_msg(user=userSet["name"], msg=last_msg)

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
{examples}
```

```CONVERSATION
{combined_history}
```

{last_msg}

```{charaSet["name"].upper()}
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
    if is_stable:
        settings = combine_settings(filtered_setting=filtered_setting)
    else:
        settings = ""
    examples = combine_examples(
        chara=charaSet["name"],
        user=userSet["name"],
        examples=charaSet["examples"],
        include_performance=True,
    )
    combined_history = combine_sayings(sayings=history, with_quotation=False)
    last_msg = history[-1]["content"]
    last_msg = extract_msg(user=userSet["name"], msg=last_msg)

    # prompts
    result = f"""```MAIN CHARACTER
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

```REQUIREMENTS
Consider {charaSet['name']}'s next performance in response to what just happened, in {charaSet['name']}'s tone and personality.
In the story, {charaSet['name']}'s physical actions should be put between brackets []. Actions and words of {charaSet['name']} should appear alternately. 
{examples}
```

```CONVERSATION
{combined_history}
```

{last_msg}

```{charaSet["name"].upper()}
{fields}
PERFORMANCE:"""

    return result
