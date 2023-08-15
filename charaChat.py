from chat import Chat
from prompts import get_begin_prompts, get_tone_prompts
import openai
import os

class CharaChat(Chat):
    def __init__(self, charaSet: dict, chatSet: dict):
        super().__init__(chatSet)
        self.chara = charaSet
        self.initMsg()
    
    def initMsg(self):
        self.history = get_begin_prompts(self.chara)
    
    def get_response(self):
        info_response = super().get_response()

        tone_response =openai.Completion.create(
            model="text-davinci-003",
            prompt=get_tone_prompts(charaSet=self.chara, 
                                    input_sentence=self.history[-1]["content"], 
                                    info_points=info_response),
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )

        tone_text = tone_response["choices"][0]["text"]
        # delete the \n at the beginning of the response
        for i in range(len(tone_text)):
            if tone_text[i] != "\n" and tone_text[i] != " ":
                tone_text = tone_text[i:]
                break

        return tone_text

    def print_history(self):
        os.system("cls")
        for i, msg in enumerate(self.history):
            if i >= 8:
                if msg["role"] == "user":
                    print("You: " + msg["content"])
                else:
                    print(self.chara["name"] + ": " + msg["content"])



