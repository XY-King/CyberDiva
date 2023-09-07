import json
from charaChat import CharaChat
from read import get_chara_config
import os 

def get_config_id():
    if os.path.exists("my_config.json"):
        return "my_config.json"
    else:
        return "config.json"

def main():
    config_id = get_config_id()
    chatSet = json.load(open(config_id, "rb"))

    if chatSet["api_key"] == "YOUR_API_KEY":
        print("Please set your API key in config.json")
        return

    charaSet = get_chara_config(chatSet["api_key"])
    userSet = json.load(open("user.json", "rb"))
    core = CharaChat(chatSet=chatSet, charaSet=charaSet, userSet=userSet)
    while True:
        core.print_history()
        user_input = input(">>> ")
        if user_input == "exit":
            break
        elif user_input == "debug":
            print(core.history)
            for msg in core.real_history:
                print(msg["content"])
            input()
        else:
            core.user_input(user_input)
            response = core.get_response()
            reaction_list = core.add_response(response=response)
            core.trigger_live2d(reaction_list)

if __name__ == "__main__":
    main()
