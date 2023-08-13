import openai
import json

openai.api_key = json.load(open("config.json"))["api_key"]


def main():
    print(openai.api_key)


if __name__ == "__main__":
    main()
