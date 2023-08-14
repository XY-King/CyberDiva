import json
from charaChat import CharaChat

def main():
    chatSet = json.load(open("config.json", "rb"))
    charaSet = json.load(open("chara.json", "rb"))
    test = CharaChat(chatSet=chatSet, charaSet=charaSet)
    myInput = input(">>> ")
    test.user_input(myInput)
    test.get_response()
    print(test.history[-1])


if __name__ == "__main__":
    main()
