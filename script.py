import json
from charaChat import CharaChat
from read import get_chara_config, get_user_config
from flask import Flask, request, render_template
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout   
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QCursor
import threading
from config import set_api_key
from utils import change_language

print("starting...")
app = Flask(__name__)
set_api_key()
app_port = 5000

@app.route("/")
def index():
    global chatSet, charaSet, userSet, core

    chatSet = json.load(open("json/config.json", "rb"))
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

def run_app():
    app.run(host="localhost", port=app_port, debug=False)

class MainWindow(QMainWindow):
    m_drag_position = None

    def __init__(self):
        super().__init__()

        # The circle widget
        self.button = QPushButton('')
        self.button.setStyleSheet("""
            QPushButton {
                background-color: purple;
                border: none;
                border-radius: 20px;
                min-width: 40px;
                min-height: 40px;
            }
        """)
        self.button.pressed.connect(self.start_drag)

        # The web view
        self.web = QWebEngineView()
        self.web.load(QUrl(f"http://localhost:{app_port}"))
        self.web.page().setBackgroundColor(Qt.transparent)
        self.web.setFixedSize(320, 720)

        # Create a layout and add the widgets
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.web)

        # Create a QWidget and set the layout
        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        # Set the central widget
        self.setCentralWidget(centralWidget)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def start_drag(self):
        MainWindow.m_drag_position = self.mapFromGlobal(QCursor.pos())
        QApplication.setOverrideCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if MainWindow.m_drag_position:
            self.move(self.mapToGlobal(event.pos()) - MainWindow.m_drag_position)

    def mouseReleaseEvent(self, event):
        QApplication.restoreOverrideCursor()
        MainWindow.m_drag_position = None

if __name__ == "__main__":
    change_language()

    t = threading.Thread(target=run_app)
    t.daemon = True
    t.start()

    appQt = QApplication([])
    window = MainWindow()
    window.show()
    appQt.exec_()
