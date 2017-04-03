import docker
from flask import Flask

app = Flask(__name__)
client = docker.from_env()


@app.route("/")
def index():
    return "Hello."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4242, use_debugger=True, use_reloader=True)
