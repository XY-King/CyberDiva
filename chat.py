import openai
import string
import os
import time
from utils import filter_history, with_embedding


class Chat:
    def __init__(self, setting: dict):
        self.setting = setting
        self.history = []

    def user_input(self, input: string):
        self.history.append(with_embedding({"role": "user", "content": input}))

    def get_response(self):
        start_time = time.time()
        filtered_history = filter_history(
            self.history, input=self.history[-1]["content"], num=256
        )
        for msg in filtered_history:
            msg.pop["embedding"]
        response = openai.ChatCompletion.create(
            model=self.setting["model"],
            messages=[self.setting["sys_msg"]] + filtered_history,
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )
        print("get_response: " + str(time.time() - start_time))
        return response.choices[0]["message"]["content"]

    def add_response(self, response: string):
        response_msg = {"role": "assistant", "content": response}
        self.history.append(with_embedding(response_msg))

    def print_history(self):
        os.system("cls")
        for msg in self.history:
            print(msg["role"] + ": " + msg["content"])
