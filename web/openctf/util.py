import random
from urllib.parse import urljoin, urlparse

from flask import redirect, request, url_for
from wtforms.validators import Required


class RequiredIf(Required):

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


def random_string(length=32, alpha="012346789abcdef"):
    """ Generates a random string of length length using characters from alpha. """
    characters = [random.choice(alpha) for x in range(length)]
    return "".join(characters)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form.get("next", url_for("users.profile"))
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)
