import string

def get_intro_prompts(charaSet: dict):
    begin = f"""You are now going to perform as an imaginary character.

Character name: {charaSet["name"]}

Character sayings: 
    """

    for saying in charaSet["sayings"]:
        begin += saying + '\n    '

    return [ {"role": "user", "content": begin}
           , {"role": "assistant", "content": f"Ok, I am now going to perform as the imaginary character {charaSet['name']}."}
           ]


info_point_prompts = [ "In the following conversation, all the information points you want to express should be in the form of a list."
                     , "Ok, let's make a sample conversation."
                     , "Would you like to have lunch with me?"
                     , "- I'd love to\n- Asking what to have for lunch"
                     , "Ok, let's now begin a real conversation."
                     ]


def get_info_point_prompts(charaSet: dict):
    result = []

    for i, prompt in enumerate(info_point_prompts):
        if i % 2 == 0:
            result.append({"role": "user", "content": prompt})
        else:
            result.append({"role": "assistant", "content": prompt})
    
    end = f"Ok, in this conversation I will perform as the imaginary character {charaSet['name']} and only cover and list the necessary information points."

    result.append({"role": "assistant", "content": end})

    return result


def get_begin_prompts(charaSet: dict):
    return get_intro_prompts(charaSet) + get_info_point_prompts(charaSet)


def get_tone_prompts(charaSet: dict, info_points: string):
    begin = f"""Here is a conversation between an imagined character called '{charaSet['name']}' and a human.
    
This is the sayings of '{charaSet['name']}':
    """

    for saying in charaSet["sayings"]:
        begin += saying + '\n    '

    info_prompt = f"These are the points {charaSet['name']} wants to express in a daily conversation:\n"
    info_prompt += info_points + '\n'
    
    end = f"Here is how {charaSet['name']} would express this in {charaSet['name']}'s tone."

    return begin + info_prompt + end
