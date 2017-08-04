import io
import string

import requests

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from PIL import Image
from sqlalchemy import func
from wtforms import ValidationError
from wtforms.fields import *
from wtforms.validators import *

from openctf.config import get_require_email_verification
from openctf.models import Activity, Config, User, db
from openctf.util import (VALID_USERNAME, get_redirect_target, random_string,
                          redirect_back, send_email)

blueprint = Blueprint("users", __name__, template_folder="templates")


@blueprint.route("/forgot", methods=["GET", "POST"])
@login_required
def forgot():
    return "forgot"


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    redirect_to = get_redirect_target()
    if current_user.is_authenticated:
        return redirect_back("users.profile")
    login_form = LoginForm(remember=True)
    if login_form.validate_on_submit():
        user = login_form.get_user()
        if not user.admin and (get_require_email_verification() and not user.email_verified):
            flash("You haven't activated your account yet! Check your email for an activation email.", "danger")
            return redirect(url_for("users.login"))
        login_user(user)
        flash("Successfully logged in!", "success")
        return redirect_back("users.profile")
    return render_template("users/login.j2", login_form=login_form, next=redirect_to)


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out!", "success")
    return redirect(url_for("base.index"))


@blueprint.route("/profile")
@blueprint.route("/profile/<int:id>")
def profile(id=None):
    if id is None and current_user.is_authenticated:
        return redirect(url_for("users.profile", id=current_user.id))
    user = User.get_by_id(id)
    if user is None:
        abort(404)
    me = user.id == current_user.id if current_user.is_authenticated else False
    return render_template("users/profile.j2", user=user, me=me)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm(prefix="register")
    if register_form.validate_on_submit():
        send_email = get_require_email_verification()
        new_user = register_user(register_form.name.data,
                                 register_form.email.data,
                                 register_form.username.data,
                                 register_form.password.data,
                                 int(register_form.level.data),
                                 send_email=send_email, admin=False)

        if send_email:
            flash("Check your email for an activation link.", "info")
            return redirect(url_for("users.login"))

        login_user(new_user)
        return redirect(url_for("users.profile"))
    return render_template("users/register.j2", register_form=register_form)


@blueprint.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    change_password_form = ChangePasswordForm(prefix="change-password")
    profile_edit_form = ProfileEditForm(prefix="profile-edit")

    if change_password_form.submit.data and change_password_form.validate_on_submit():
        current_user.password = change_password_form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash("Password changed.", "success")
        return redirect(url_for("users.settings"))

    if profile_edit_form.validate_on_submit() and profile_edit_form.submit.data:
        for field in profile_edit_form:
            if field.short_name == "avatar":
                if len(field.data.read()) > 0:
                    field.data.seek(0)
                    response = requests.post("{}/save".format(current_app.config["FILESTORE_URL"]),
                                             data={"prefix": "avatar"},
                                             files={"file": field.data})
                    if response.status_code == 200:
                        current_user._avatar = "/static/{}".format(response.text)
                continue
            if hasattr(current_user, field.short_name):
                setattr(current_user, field.short_name, field.data)
        if profile_edit_form.remove_avatar.data:
            current_user._avatar = None
        db.session.add(current_user)
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("users.settings"))
    else:
        for field in profile_edit_form:
            if hasattr(current_user, field.short_name):
                field.data = getattr(current_user, field.short_name, "")
    return render_template("users/settings.j2",
                           change_password_form=change_password_form,
                           profile_edit_form=profile_edit_form)


@blueprint.route("/verify/<token>")
def verify(token):
    user = User.query.filter_by(email_token=token).first()
    if user:
        if user.email_verified:
            flash("Email is already verified.", "info")
            return redirect(url_for("users.profile"))
        if user.email_token == token:
            user.email_verified = True
            flash("Email has been verified!", "success")
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("users.profile"))

    flash("Invalid token.", "danger")
    return redirect(url_for("users.login"))


def register_user(name, email, username, password, level, admin=False, send_email=True, **kwargs):
    new_user = User(name=name, username=username, password=password, email=email, level=level, admin=admin)
    for key, value in kwargs.items():
        setattr(new_user, key, value)
    code = random_string()
    new_user.email_token = code
    if send_email:
        send_verification_email(username, email, url_for("users.verify", token=code, _external=True))
    db.session.add(new_user)
    db.session.commit()

    activity = Activity(uid=new_user.id, _type=Activity.REGISTERED)
    db.session.add(activity)
    db.session.commit()
    return new_user


def send_verification_email(username, email, link):
    ctf_name = Config.get("ctf_name")
    subject = "[ACTION REQUIRED] Email Verification - {}".format(ctf_name)
    body = string.Template(Config.get("email_body")).substitute(
        ctf_name=ctf_name,
        link=link,
        username=username,
    )
    response = send_email(email, subject, body)
    if response.status_code != 200:
        raise Exception("Failed: {}".format(response.text))
    response = response.json()
    if "Queued" in response["message"]:
        return True
    else:
        raise Exception(response["message"])


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[
        InputRequired("Please enter your old password.")])
    password = PasswordField("Password", validators=[
        InputRequired("Please enter a password.")])
    confirm_password = PasswordField("Confirm Password", validators=[
        InputRequired("Please confirm your password."),
        EqualTo("password", "Please enter the same password.")])
    submit = SubmitField("Update Password")

    def validate_old_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError("Old password doesn't match.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("Please enter your username.")])
    password = PasswordField("Password", validators=[InputRequired("Please enter your password.")])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

    def get_user(self):
        query = User.query.filter(func.lower(User.username) == self.username.data.lower())
        return query.first()

    def validate_username(self, field):
        if self.get_user() is None:
            raise ValidationError("This user doesn't exist.")

    def validate_password(self, field):
        user = self.get_user()
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError("Check your password again.")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired("Please enter a name.")])
    username = StringField("Username", validators=[InputRequired("Please enter a username."), Length(3, 24, "Your username must be between 3 and 24 characters long.")])
    email = StringField("Email", validators=[InputRequired("Please enter an email."), Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[InputRequired("Please enter a password.")])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired("Please confirm your password."), EqualTo("password", "Please enter the same password.")])
    level = RadioField("Who are you?", choices=[("1", "Student"), ("2", "Observer"), ("3", "Teacher")])
    github_id = HiddenField(validators=[Optional()])
    google_id = HiddenField(validators=[Optional()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if not VALID_USERNAME.match(field.data):
            raise ValidationError("Username must be contain letters, numbers, or _, and not start with a number.")
        if User.query.filter(func.lower(User.username) == field.data.lower()).count():
            raise ValidationError("Username is taken.")

    def validate_email(self, field):
        if User.query.filter(func.lower(User.email) == field.data.lower()).count():
            raise ValidationError("Email is taken.")


class ProfileEditForm(FlaskForm):
    name = StringField("Name",
                       validators=[InputRequired("Please enter a name.")])
    avatar = FileField("Avatar")
    remove_avatar = BooleanField("Remove Avatar")
    submit = SubmitField("Update Profile")

    def validate_avatar(self, field):
        try:
            data = field.data.read()
            if data:
                field.data.seek(0)
                Image.open(io.BytesIO(data))
        except:
            raise ValidationError("Please upload an image")
