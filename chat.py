import openai


class Chat:
    def __init__(self, model_id, sys_msg, api_key, max_tokens, temperature):
        self.model_id = model_id
        self.sys_msg = sys_msg
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.history = []

    def user_input(self, input):
        input_msg = {"role": "user", "content": input}
        self.history.append(input_msg)

    def get_response(self):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=self.history,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        response_msg = {"role": "assistant",
                        "content": response.choices[0].text}
        self.history.append(response_msg)
