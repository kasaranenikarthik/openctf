from flask import Flask, redirect, request, url_for

import openctf.views as views
from openctf.config import (Config, get_allow_registrations, get_ctf_name,
                            setup_complete)
from openctf.extensions import cache, login_manager, make_celery
from openctf.models import db


def create_app(config=None, name=__name__):
    app = Flask(name, static_folder="assets")
    if not config:
        config = Config()
    with app.app_context():
        # import config
        app.config.from_object(config)

        # setup handler
        @app.before_request
        def check_setup_completed():
            if request.path.startswith("/assets"):
                return
            if not setup_complete() and request.path != url_for("base.setup"):
                return redirect(url_for("base.setup"))

        # inject jinja variables
        app.jinja_env.globals.update(get_ctf_name=get_ctf_name)
        app.jinja_env.globals.update(get_allow_registrations=get_allow_registrations)

        # configure extensions
        cache.init_app(app)
        make_celery(app)
        db.init_app(app)
        login_manager.init_app(app)

        # register blueprints
        app.register_blueprint(views.admin.blueprint, url_prefix="/admin")
        app.register_blueprint(views.base.blueprint)
        app.register_blueprint(views.users.blueprint, url_prefix="/users")

        return app
