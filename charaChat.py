import string
from chat import Chat
from prompts import get_begin_prompts, get_tone_prompts, filter_sayings
import openai
from openai.embeddings_utils import get_embedding
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
            sayings=self.chara["sayings"],
            input=input,
            api_key=self.setting["api_key"],
            num=20,
        )
        filtered_story = filter_sayings(
            sayings=self.chara["story"],
            input=input,
            api_key=self.setting["api_key"],
            num=2,
        )

        self.filtered_setting = {"sayings": filtered_saying, "story": filtered_story}

    def user_input(self, input: string):
        self.get_filtered_setting(input)

        init_msg = get_begin_prompts(
            charaSet=self.chara,
            userSet=self.user,
            filtered_setting=self.filtered_setting,
        )
        named_input = self.user["name"] + ": " + input

        if self.history == []:
            for msg in init_msg:
                self.history.append(msg)
        else:
            for i, msg in enumerate(init_msg):
                self.history[i] = msg
        super().user_input(named_input)
        self.real_history.append(
            with_embedding({"role": "user", "content": input}, self.setting["api_key"])
        )

    def add_response(self, response: string):
        tone_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=get_tone_prompts(
                setting=self.setting, 
                charaSet=self.chara,
                userSet=self.user,
                history=self.real_history,
                info_points=response,
                filtered_setting=self.filtered_setting,
                api_key=self.setting["api_key"],
            ),
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )

        tone_text = tone_response["choices"][0]["text"]
        # delete the nonsense at the beginning of the response
        for i in range(len(tone_text)):
            if not tone_text[i] in ["\n", " ", '"']:
                tone_text = tone_text[i:]
                break

        self.history.append({"role": "assistant", "content": response})
        self.real_history.append(
            with_embedding(
                {"role": "assistant", "content": tone_text}, self.setting["api_key"]
            )
        )

    def print_history(self):
        os.system("cls")
        for _msg in self.real_history:
            msg = _msg["content"]
            if msg["role"] == "user":
                print("You: " + msg["content"])
            else:
                print(self.chara["name"] + ": " + msg["content"])


# HELPER FUNCTIONS


def with_embedding(msg: dict, api_key: string):
    openai.api_key = api_key
    embedding = get_embedding(text=msg["content"], engine="text-embedding-ada-002")
    return {"content": msg, "embedding": embedding}
