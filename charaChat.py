from chat import Chat
from prompts import get_begin_prompts, get_tone_prompts
import openai

class CharaChat(Chat):
    def __init__(self, charaSet: dict, chatSet: dict):
        super().__init__(chatSet)
        self.chara = charaSet
        self.initMsg()
    
    def initMsg(self):
        self.history = get_begin_prompts(self.chara)
    
    # override the get_response method
    def get_response(self):
        openai.api_key = self.setting["api_key"]
        response = openai.ChatCompletion.create(
            model=self.setting["model"],
            messages=self.history,
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )

        tone_response =openai.Completion.create(
            model="text-davinci-003",
            prompt=get_tone_prompts(self.chara, response.choices[0]["message"]["content"]),
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )

        response_msg = {"role": "assistant",
                        "content": tone_response.choices[0]["text"]}
        self.history.append(response_msg)


