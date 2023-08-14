from chat import Chat
from setting import charaSetting, chatSetting
from prompts import get_begin_prompts


class CharaChat(Chat):
    def __init__(self, charaSet: charaSetting, chatSet: chatSetting):
        super().__init__(chatSet)
        self.chara = charaSet
        self.initMsg()
    
    def initMsg(self):
        self.history.append(get_begin_prompts(self.chara))
