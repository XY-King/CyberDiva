import json
from charaChat import CharaChat

def main():
    chatSet = json.load(open("config.json", "rb"))
    charaSet = json.load(open("chara.json", "rb"))
    core = CharaChat(chatSet=chatSet, charaSet=charaSet)
    while True:
        core.print_history()
        user_input = input(">>> ")
        if user_input == "exit":
            break
        else:
            core.user_input(user_input)
            core.add_response(core.get_response())


if __name__ == "__main__":
    main()
