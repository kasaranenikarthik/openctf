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
