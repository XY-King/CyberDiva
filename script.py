import json
from charaChat import CharaChat
from read import get_chara_config, get_user_config, get_api_key
import os
from flask import Flask, request, render_template


def get_key_id():
    if os.path.exists("my_key.json"):
        return "my_key.json"
    else:
        return "key.json"


def get_user_id():
    if os.path.exists("my_user.json"):
        return "my_user.json"
    else:
        return "user.json"


app = Flask(__name__)
get_api_key(get_key_id())


@app.route("/")
def index():
    global chatSet, charaSet, userSet, core

    chatSet = json.load(open("config.json", "rb"))
    charaSet = get_chara_config()
    userSet = get_user_config(get_user_id(), charaSet["name"])
    core = CharaChat(chatSet=chatSet, charaSet=charaSet, userSet=userSet)

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global core

    data = request.get_json()
    user_input = data.get("user_input")
    print(user_input)
    core.user_input(user_input)
    response = core.get_response()
    action_list = core.add_response(response=response)
    # core.trigger_live2d(reaction_list)
    for reaction in action_list:
        print(reaction)
    return {"action_list": action_list}


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
