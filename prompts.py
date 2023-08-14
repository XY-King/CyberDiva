from setting import charaSetting

def get_intro_prompts(charaSet: charaSetting):
    begin = f"""You are now going to perform as an imaginary character.

Character name: {charaSet.name}

Character sayings: 
    """

    for saying in charaSet.sayings:
        begin += saying + '\n    '

    return [ {"role": "user", "content": begin}
           , {"role": "assistant", "content": f"Ok, I am now going to perform as the imaginary character {charaSet.name}."}
           ]

info_point_prompts = [ "In the following conversation, only the necessary information points should be covered and listed."
                     , "Ok, let's make a sample conversation."
                     , "Would you like to have lunch with me?"
                     , "- I'd love to\n- Asking what to have for lunch"
                     , "Ok, let's now begin a real conversation."
                     ]

def get_info_point_prompts(charaSet: charaSetting):
    result = []

    for i, prompt in enumerate(info_point_prompts):
        if i % 2 == 0:
            result.append({"role": "user", "content": prompt})
        else:
            result.append({"role": "assistant", "content": prompt})
    
    end = f"Ok, in this conversation I will perform as the imaginary character {charaSet.name} and only cover and list the necessary information points."

    result.append({"role": "assistant", "content": end})

    return result

def get_begin_prompts(charaSet: charaSetting):
    return get_intro_prompts(charaSet) + get_info_point_prompts(charaSet)