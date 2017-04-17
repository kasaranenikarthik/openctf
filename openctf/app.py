from json import dumps

import docker
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

socketio = SocketIO(app)
client = docker.from_env()


def status():
    return "shiet"


@socketio.on("status")
def status_handler():
    return dumps(status())


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=4242, use_reloader=True)
