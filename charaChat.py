from chat import Chat


class CharaChat(Chat):
    def __init__(self, charaInfo, model_id, sys_msg, api_key, max_tokens, temperature):
        super().__init__(model_id, sys_msg, api_key, max_tokens, temperature)
        self.charaInfo = charaInfo
