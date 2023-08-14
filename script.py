import json
from charaChat import CharaChat

def main():
    chatSet = json.load(open("config.json", "rb"))
    charaSet = json.load(open("chara.json", "rb"))
    test = CharaChat(chatSet=chatSet, charaSet=charaSet)
    print(test.history)


if __name__ == "__main__":
    main()
