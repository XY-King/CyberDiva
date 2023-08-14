from setting import charaSetting


def begin_prompts(charaSet: charaSetting):
    begin = f"""
You are now going to perform as an imaginary character。

Character name: {charaSet.name}

Character sayings: 
    """

    for saying in charaSet.sayings:
        begin += saying + '\n    '

    return [ {"role": "user", "content": begin}
           , {"role": "assistant", "content": f"Ok, I am now going to perform as the imaginary character {charaSet.name}."}
        ]
