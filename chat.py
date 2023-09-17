import openai
import string
import os
import time

class Chat:
    def __init__(self, setting : dict):
        self.setting = setting
        self.history = []

    def user_input(self, input: string):
        input_msg = {"role": "user", "content": input}
        self.history.append(input_msg)

    def get_response(self):
        start_time = time.time()
        response = openai.ChatCompletion.create(
            model=self.setting["model"],
            messages=[self.setting["sys_msg"]] + self.history,
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )
        print("get_response: " + str(time.time() - start_time))
        return response.choices[0]["message"]["content"]
    
    def add_response(self, response: string):
        response_msg = {"role": "assistant",
                        "content": response}
        self.history.append(response_msg)
    
    def print_history(self):
        os.system("cls")
        for msg in self.history:
            print(msg["role"] + ": " + msg["content"])
