import string
from chat import Chat
from prompts import get_begin_prompts, get_tone_prompts, filter_sayings
import openai
import os

class CharaChat(Chat):
    def __init__(self, charaSet: dict, chatSet: dict, userSet: dict):
        super().__init__(chatSet)
        self.chara = charaSet
        self.user = userSet
        self.real_history = []
        self.filtered_setting = []
    
    def get_filtered_setting(self, input: string):
        filtered_saying = filter_sayings(
            sayings=self.charaSet["sayings"], input=input, api_key=self.setting["api_key"], num=10
        )
        filtered_story = filter_sayings(
            sayings=self.charaSet["story"], input=input, api_key=self.setting["api_key"], num=3
        )

        self.filtered_setting = {"sayings": filtered_saying, "story": filtered_story}

    def user_input(self, input: string):
        self.get_filtered_setting(input)

        init_msg = get_begin_prompts(charaSet=self.chara, userSet=self.user, filtered_setting=self.filtered_setting)
        named_input = self.user["name"] + ": \n" + input

        if self.history == []:
            for msg in init_msg:
                self.history.append(msg)
        else:
            for i, msg in enumerate(init_msg):
                self.history[i] = msg
        super().user_input(named_input)
        self.real_history.append({"role": "user", "content": input})

    def add_response(self, response: string):
        tone_response =openai.Completion.create(
            model="text-davinci-003",
            prompt=get_tone_prompts(charaSet=self.chara, 
                                    history=self.real_history,
                                    info_points=response),
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )

        tone_text = tone_response["choices"][0]["text"]
        # delete the \n at the beginning of the response
        for i in range(len(tone_text)):
            if tone_text[i] != "\n" and tone_text[i] != " ":
                tone_text = tone_text[i:]
                break
        
        self.history.append({"role": "assistant", "content": response})
        self.real_history.append({"role": "assistant", "content": tone_text})
        

    def print_history(self):
        os.system("cls")
        for i, msg in enumerate(self.real_history):
            if msg["role"] == "user":
                print("You: " + msg["content"])
            else:
                print(self.chara["name"] + ": " + msg["content"])



