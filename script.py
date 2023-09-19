import json
from charaChat import CharaChat
from read import get_chara_config, get_user_config, get_api_key
import os
from flask import Flask, request, render_template

app = Flask(__name__)
get_api_key()


@app.route("/")
def index():
    global chatSet, charaSet, userSet, core

    chatSet = json.load(open("config.json", "rb"))
    charaSet = get_chara_config()
    userSet = get_user_config(charaSet["name"])
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
    for reaction in action_list:
        print(reaction)
    return {"action_list": action_list}


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
