from chat import Chat


class CharaChat(Chat):
    def __init__(self, charaSet, chatSet):
        super().__init__(chatSet)
        self.chara = charaSet
    
    
