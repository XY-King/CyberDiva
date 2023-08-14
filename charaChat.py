from chat import Chat
from setting import charaSetting, chatSetting


class CharaChat(Chat):
    def __init__(self, charaSet: charaSetting, chatSet: chatSetting):
        super().__init__(chatSet)
        self.chara = charaSet
        self.initMsg()
    
    def initMsg(self):
        begin = f"You are now going to perform as an imaginary character\n\n"
