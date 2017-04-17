import traceback
from json import dumps

import docker
from flask import Flask, render_template
from flask_socketio import SocketIO

import api

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

socketio = SocketIO(app)
client = docker.from_env()

# All required/optional components for OpenCTF
#   buildpath: Path (local URL)
#   name: Name of the service.
#   require: Whether it's required or not.
#   single: Whether this service must be limited to a single instance or not.
components = [
    {"name": "cache", "required": True, "single": True},
    {"name": "db", "required": True, "single": True},
    {"name": "filestore", "required": True, "single": True},
    {"name": "web", "required": True},
]


def status():
    try:
        data = dict()
        data["components"] = []
        for component in components:
            cdata = dict()
            cdata["name"] = component["name"]
            data["components"].append(cdata)
        return data
    except:
        return dict(error=traceback.format_exc())


@socketio.on("status")
def status_handler():
    return dumps(status())


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=4242, use_reloader=True)
