import string
from chat import Chat
from prompts import (
    get_begin_prompts,
    get_tone_prompts,
    filter_info_points,
)
from read import get_chara_setting_keys
import openai
import time
from utils import filter_sayings, combine_sayings, with_embedding, filter_history


class CharaChat(Chat):
    def __init__(self, charaSet: dict, chatSet: dict, userSet: dict):
        super().__init__(chatSet)
        self.chara = charaSet
        self.user = userSet
        self.real_history = []
        self.filtered_setting = []

    def get_filtered_setting(self, input: string):
        TOTAL_LENGTH = 5000
        self.filtered_setting = {}
        # get the keys in the charaInit for character setting
        keys = get_chara_setting_keys(self.chara["name"])
        # allocate the number of sayings to be filtered for each key
        values_total_length = 0
        for key in keys:
            for value in self.chara[key]:
                values_total_length += len(value["content"])
        # filter the settings
        for key in keys:
            values = self.chara[key]
            filter_num = int(TOTAL_LENGTH * (len(values) / values_total_length))
            filtered_values = filter_sayings(
                sayings=values,
                input=input,
                num=filter_num,
            )
            self.filtered_setting[key] = combine_sayings(filtered_values)

    def user_input(self, input: string):
        start_time = time.time()
        named_input = self.user["name"] + ": " + input
        super().user_input(named_input)
        self.real_history.append(with_embedding({"role": "user", "content": input}))
        print("user_input: " + str(time.time() - start_time))

    def get_response(self):
        start_time = time.time()
        filtered_history = filter_history(
            self.history, input=self.history[-1]["content"], num=256
        )
        for msg in filtered_history:
            msg.pop("embedding")

        self.get_filtered_setting(self.history[-1]["content"])
        init_msg = get_begin_prompts(
            charaSet=self.chara,
            userSet=self.user,
            filtered_setting=self.filtered_setting,
        )
        response = openai.ChatCompletion.create(
            model=self.setting["model"],
            messages=[self.setting["sys_msg"]] + init_msg + filtered_history,
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )
        print("get_response: " + str(time.time() - start_time))
        return response.choices[0]["message"]["content"]

    def add_response(self, response: string):
        start_time = time.time()
        response = filter_info_points(
            info_points=response,
            input=self.history[-1]["content"],
            charaSet=self.chara,
        )
        print("filter_info_points: " + str(time.time() - start_time))
        start_time = time.time()
        tone_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=get_tone_prompts(
                setting=self.setting,
                charaSet=self.chara,
                userSet=self.user,
                history=self.real_history,
                info_points=response,
                filtered_setting=self.filtered_setting,
            ),
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
            presence_penalty=self.setting["presence_penalty"],
        )

        tone_prompt = get_tone_prompts(
            setting=self.setting,
            charaSet=self.chara,
            userSet=self.user,
            history=self.real_history,
            info_points=response,
            filtered_setting=self.filtered_setting,
        )
        # output the prompt to a file
        with open("prompt.txt", "w", encoding="UTF-8") as f:
            f.write(tone_prompt)

        tone_text = tone_response["choices"][0]["text"]
        tone_text = clean_response(tone_text)

        self.history.append(
            with_embedding(
                {
                    "role": "assistant",
                    "content": response,
                }
            )
        )
        self.real_history.append(
            with_embedding(
                {
                    "role": "assistant",
                    "content": tone_text,
                }
            )
        )
        print("add_response: " + str(time.time() - start_time))
        return pair_response_list(
            response_list=seperate_response(tone_text, self.chara),
            chara_motions=self.chara["motions"],
        )

    def print_history(self):
        # os.system("cls")
        for _msg in self.real_history:
            msg = _msg["content"]
            if msg["role"] == "user":
                print("You: " + msg["content"])
            else:
                print(self.chara["name"] + ": " + msg["content"])

# HELPER FUNCTIONS


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
    # clear all the \" in the response
    response = response.replace('"', "")
    return response


def seperate_response(response: string, charaSet: dict):
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

            # remove the character name from the motion
            content_in = content_in.replace(charaSet["name"], "")
            response_list.append({"type": "motion", "content": content_in})
            response = content_after

    return response_list


def pair_response_list(response_list: list, chara_motions: list):
    def get_motion(motion: string):
        motion = filter_sayings(
            sayings=chara_motions,
            input=motion,
            num=1,
        )[
            0
        ]["content"]
        return motion

    response_pairs = []
    # pair the motion and text in the response_list together
    for i in range(0, len(response_list), 2):
        if i == len(response_list) - 1:
            if response_list[i]["type"] == "motion":
                motion = get_motion(response_list[i]["content"])
                response_pairs.append({"motion": motion, "text": ""})
            else:
                text = response_list[i]["content"]
                response_pairs.append({"motion": "", "text": text})
            break
        if response_list[i]["type"] == "motion":
            motion = get_motion(response_list[i]["content"])
            text = response_list[i + 1]["content"]
            response_pairs.append({"motion": motion, "text": text})
        else:
            motion = get_motion(response_list[i + 1]["content"])
            text = response_list[i]["content"]
            response_pairs.append({"motion": motion, "text": text})
    return response_pairs
