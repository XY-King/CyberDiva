import openai
import string
import os

class Chat:
    def __init__(self, setting : dict):
        self.setting = setting
        self.history = []

    def user_input(self, input: string):
        input_msg = {"role": "user", "content": input}
        self.history.append(input_msg)

    def get_response(self):
        openai.api_key = self.setting["api_key"]
        response = openai.ChatCompletion.create(
            model=self.setting["model"],
            messages=self.history,
            max_tokens=self.setting["max_tokens"],
            temperature=self.setting["temperature"],
        )
        return response.choices[0].text
    
    def add_response(self, response: string):
        response_msg = {"role": "assistant",
                        "content": response.choices[0].text}
        self.history.append(response_msg)
    
    def print_history(self):
        os.system("cls")
        for i, msg in enumerate(self.history):
            if i >= 8:
                print(msg["role"] + ": " + msg["content"])
