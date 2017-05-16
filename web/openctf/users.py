from openctf.models import db, User
from openctf.util import random_string


def register_user(name, email, username, password, level, admin=False, send_email=True):
    new_user = User(name=name, username=username, password=password, email=email, level=level, admin=admin)
    code = random_string()
    new_user.email_token = code
    if send_email:
        send_verification_email(username, email, url_for("users.verify", code=code, _external=True))
    db.session.add(new_user)
    db.session.commit()
    return new_user
