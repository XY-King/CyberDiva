import openai
import string
import os
import time
import numpy as np
from utils import filter_history
from config import get_embedding


class Chat:
    def __init__(self, setting: dict):
        self.setting = setting
        self.history = {"content": [], "embedding": []}

    def user_input(self, input: string):
        self.history["content"].append({"role": "user", "content": input})
        self.history["embedding"].append(get_embedding(input))

    def get_response(self):
        start_time = time.time()
        filtered_history = filter_history(
            history=self.history["content"],
            history_embeddings=self.history["embedding"],
            input=self.history["content"][-1]["content"],
            num=256,
        )
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
        self.history["content"].append(response_msg)
        self.history["embedding"].append(get_embedding(response))

    def print_history(self):
        os.system("cls")
        for msg in self.history["content"]:
            print(msg["role"] + ": " + msg["content"])
