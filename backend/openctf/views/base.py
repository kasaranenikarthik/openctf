import sys

from flask import Blueprint, abort, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import *
from wtforms.validators import *
from datetime import datetime, timedelta

from openctf.config import (generate_verification_token, get_ctf_name,
                            setup_complete)
from openctf.extensions import cache
from flask_login import login_user
from openctf.models import Config, db
from openctf.users import register_user

blueprint = Blueprint("base", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    return render_template("base/index.j2")


@blueprint.route("/setup", methods=["GET", "POST"])
def setup():
    if setup_complete():
        return abort(404)
    if Config.get("setup_verification") is None:
        # generate setup verification token
        generate_verification_token()
    setup_form = SetupForm()
    setup_form.admin_user.data = "root"
    if setup_form.validate_on_submit():
        form_fields = ["ctf_name", "team_size", "admin_email"]
        to_update = dict()
        for field in setup_form:
            if field.short_name in form_fields:
                to_update[field.short_name] = field.data
        admin_user = register_user("Administrator", setup_form.admin_email.data, "root",
                                   setup_form.password.data, 0, admin=True, send_email=False)
        login_user(admin_user, remember=True)
        to_update.update(admin_uid=admin_user.id)
        to_update.update(allow_registrations=0)
        to_update.update(require_email_verification=0)
        to_update.update(setup_complete=1)
        now = datetime.now()
        to_update.update(start_time=(now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
        to_update.update(end_time=(now + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"))
        Config.set_many(to_update)
        cache.delete_memoized(get_ctf_name)
        cache.delete_memoized(setup_complete)
        return redirect(url_for("base.index"))
    return render_template("base/setup.j2", setup_form=setup_form)


class SetupForm(FlaskForm):
    ctf_name = StringField("CTF Name", validators=[InputRequired("Please enter a CTF name.")])
    team_size = IntegerField("Team Size", default=5, validators=[InputRequired("Please enter a max team size.")])

    admin_user = StringField("Username", render_kw=dict(readonly=True))
    admin_email = StringField("Email", validators=[InputRequired("Please enter an email."), Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[InputRequired("Please enter a password.")])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired("Please confirm your password."), EqualTo("password", "Please enter the same password.")])

    verification = StringField("Verification", validators=[InputRequired("Please enter a verification code.")])
    submit = SubmitField("Create CTF")

    def validate_username(self, field):
        if not util.VALID_USERNAME.match(field.data):
            raise ValidationError("Username must be contain letters, numbers, or _, and not start with a number.")

    def validate_verification(self, field):
        code = Config.get("setup_verification")
        if code is None or code != field.data:
            raise ValidationError("Verification failed.")
