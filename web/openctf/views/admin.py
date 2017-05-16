from flask import Blueprint

blueprint = Blueprint("admin", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    return "overview"


@blueprint.route("/settings")
def settings():
    return "settings"
