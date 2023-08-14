import openai
import string


class Chat:
    def __init__(self, setting):
        self.setting = setting
        self.history = []

    def user_input(self, input: string):
        input_msg = {"role": "user", "content": input}
        self.history.append(input_msg)

    def get_response(self):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.setting.model_id,
            messages=self.setting.history,
            max_tokens=self.setting.max_tokens,
            temperature=self.setting.temperature
        )
        response_msg = {"role": "assistant",
                        "content": response.choices[0].text}
        self.history.append(response_msg)
