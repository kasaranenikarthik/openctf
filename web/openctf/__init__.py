r"""
   ____                    _____ _______ ______
  / __ \                  / ____|__   __|  ____|
 | |  | |_ __   ___ _ __ | |       | |  | |__
 | |  | | '_ \ / _ \ '_ \| |       | |  |  __|
 | |__| | |_) |  __/ | | | |____   | |  | |
  \____/| .__/ \___|_| |_|\_____|  |_|  |_|
        | |
        |_|
            Open-source CTF Platform
       https://github.com/easyctf/openctf
"""

from flask import Flask


def create_app(config=None):
    """ Create a Flask app to be used externally. """

    app = Flask(__name__, static_folder="assets", static_path="/assets")

    if not config:
        from openctf.config import Config
        config = Config
    app.config.from_object(config)

    return app
