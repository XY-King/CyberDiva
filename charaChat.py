import string
from chat import Chat
from prompts import (
    get_begin_prompts,
    get_tone_prompts,
    filter_sayings,
    filter_info_points,
)
import openai
from openai.embeddings_utils import get_embedding
import os
import json
import asyncio
import websockets


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
        response = filter_info_points(
            info_points=response,
            input=self.history[-1]["content"],
            api_key=self.setting["api_key"],
            charaSet=self.chara,
        )
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
        tone_text = clean_response(tone_text)

        self.history.append({"role": "assistant", "content": response})
        self.real_history.append(
            with_embedding(
                {
                    "role": "assistant",
                    "content": tone_text,
                },
                self.setting["api_key"],
            )
        )
        return seperate_response(tone_text)

    def print_history(self):
        os.system("cls")
        for _msg in self.real_history:
            msg = _msg["content"]
            if msg["role"] == "user":
                print("You: " + msg["content"])
            else:
                print(self.chara["name"] + ": " + msg["content"])

    def trigger_live2d(self, response_list: list):
        for response in response_list:
            if response["type"] == "motion":
                msg = {
                    "msg": 13200,
                    "msgId": 1,
                    "data": {"id": 0, "type": 0, "mtn": motion},
                }

        text_msg = {
            "msg": 11000,
            "msgId": 1,
            "data": {
                "id": 0,
                "text": msg,
                "textFrameColor": 0x000000,
                "textColor": 0xFFFFFF,
                "duration": 10000,
            },
        }

        motion_msg = {
            "msg": 13200,
            "msgId": 1,
            "data": {"id": 0, "type": 0, "mtn": motion},
        }

        async def send_message():
            async with websockets.connect("ws://127.0.0.1:10086/api") as ws:
                message = motion_msg
                await ws.send(json.dumps(message))
                message = text_msg
                await ws.send(json.dumps(message))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_message())


# HELPER FUNCTIONS
def with_embedding(msg: dict, api_key: string):
    openai.api_key = api_key
    embedding = get_embedding(text=msg["content"], engine="text-embedding-ada-002")
    return {"content": msg, "embedding": embedding}

# def get_closest_motion(response: string, motions: list):


def clean_response(response: string):
    # delete the nonsense at the beginning of the response
    for i in range(len(response)):
        if not response[i] in ["\n", " ", '"']:
            response = response[i:]
            break
    # delete the nonsense at the end of the response
    for i in range(len(response) - 1, -1, -1):
        if not response[i] in ["\n", " ", '"']:
            response = response[: i + 1]
            break
    return response


def seperate_response(response: string):
    response_list = []
    # seperate the response into a list of strings by contents in brackets
    while True:
        if not "[" in response:
            if not response in ["", "\n", " ", '"']:
                response_list.append({"type": "text", "content": response})
            break
        else:
            left = response.index("[")
            right = response.index("]")
            content_in = response[left + 1 : right]
            content_before = response[:left]
            content_after = response[right + 1 :]
            if not content_before in ["", "\n", " ", '"']:
                response_list.append({"type": "text", "content": content_before})
            response_list.append({"type": "motion", "content": content_in})
            response = content_after

    return response_list
