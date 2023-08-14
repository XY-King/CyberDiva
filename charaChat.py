from chat import Chat
from setting import CharaSetting, ChatSetting
from prompts import get_begin_prompts


class CharaChat(Chat):
    def __init__(self, charaSet: CharaSetting, chatSet: ChatSetting):
        super().__init__(chatSet)
        self.chara = charaSet
        self.initMsg()
    
    def initMsg(self):
        self.history = get_begin_prompts(self.chara)
