from flask import abort
from flask_login import current_user

from functools import wraps


def admin_required(f):
    """
    Only allows users with admin privileges to access the endpoint that
    this function is wrapping. Users that are not logged in will also be
    denied access.

    :param func: The function that is to be wrapped.
    :return: The wrapped function.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.admin):
            abort(403)
        return f(*args, **kwargs)

    return wrapper

def team_required(f):
    """
    Only allows users who have teams (created or joined a team) to access the
    endpoint that this function is wrapping. Users that are not logged in
    will also be denied access.

    :param f: The function that is to be wrapped.
    :return: The wrapped function.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.level != 3 and \
            (not hasattr(current_user, "team") or not current_user.tid):
            flash("You need a team to view this page!", "info")
            return redirect(url_for("teams.create"))
        return f(*args, **kwargs)

    return wrapper

def block_before_competition(f):
    """
    Denied access to the endpoint that this function is wrapping from users
    before the competition start time. The competition start time can be set
    in the administration panel.

    :param f: The function that is to be wrapped.
    :return: The wrapped function.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = Config.get("start_time")
        if not start_time or not (
                current_user.is_authenticated and current_user.admin) and \
                datetime.now() < datetime.fromtimestamp(int(start_time)):
            abort(403)
        return f(*args, **kwargs)

    return wrapper


def block_after_competition(f):
    """
    Denied access to the endpoint that this function is wrapping from users
    after the competition start time. The competition start time can be set in
    the administration panel.

    :param f: The function that is to be wrapped.
    :return: The wrapped function.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        end_time = Config.get("end_time")
        if not end_time or not (
                current_user.is_authenticated and current_user.admin) \
            and datetime.now() > datetime.fromtimestamp(
                int(end_time)):
            abort(403)
        return f(*args, **kwargs)

    return wrapper
