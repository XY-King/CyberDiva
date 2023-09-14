import json
from charaChat import CharaChat
from read import get_chara_config, get_user_config
import os
from flask import Flask, request, render_template

app = Flask(__name__)


def get_config_id():
    if os.path.exists("my_config.json"):
        return "my_config.json"
    else:
        return "config.json"


def get_user_id():
    if os.path.exists("my_user.json"):
        return "my_user.json"
    else:
        return "user.json"


@app.route("/")
def index():
    global chatSet, charaSet, userSet, core

    config_id = get_config_id()
    chatSet = json.load(open(config_id, "rb"))
    if chatSet["api_key"] == "YOUR_API_KEY":
        return {"error": "Please set your API key in config.json"}

    charaSet = get_chara_config(chatSet["api_key"])
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
