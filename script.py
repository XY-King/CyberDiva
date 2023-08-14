import openai
import json
from setting import charaSetting
from prompts import begin_prompt

openai.api_key = json.load(open("config.json"))["api_key"]


def main():
    pass


if __name__ == "__main__":
    main()
