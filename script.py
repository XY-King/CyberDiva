import json
from setting import ChatSetting, CharaSetting
from charaChat import CharaChat

def main():
    api_key = json.load(open("config.json"))["api_key"]
    chatSet = ChatSetting( model_id="gpt-3.5-turbo-16k"
                         , sys_msg="You are a helpful assistant."
                         , api_key=api_key
                         , max_tokens=256
                         , temperature=1.0
    )
    charaSet = CharaSetting( name="test"
                           , sayings=["Hello", "Lala"]
    )
    test = CharaChat(chatSet=chatSet, charaSet=charaSet)
    print(test.history)


if __name__ == "__main__":
    main()
