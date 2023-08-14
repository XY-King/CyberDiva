class ChatSetting:
    def __init__(self, model_id, sys_msg, api_key, max_tokens, temperature):
        self.model_id = model_id
        self.sys_msg = sys_msg
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.temperature = temperature


class CharaSetting:
    def __init__(self, name, sayings):
        self.name = name
        self.sayings = sayings
