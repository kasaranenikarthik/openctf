from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import ValidationError
from wtforms.fields import *
from wtforms.validators import *

from openctf.config import get_require_email_verification
from openctf.models import User, db
from openctf.util import (VALID_USERNAME, get_redirect_target, random_string,
                          redirect_back)

blueprint = Blueprint("users", __name__, template_folder="templates")


@blueprint.route("/forgot", methods=["GET", "POST"])
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
    return render_template("users/profile.j2", user=user)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm(prefix="register")
    if register_form.validate_on_submit():
        new_user = register_user(register_form.name.data,
                                 register_form.email.data,
                                 register_form.username.data,
                                 register_form.password.data,
                                 int(register_form.level.data),
                                 send_email=False, admin=False)
        login_user(new_user)
        return redirect(url_for("users.profile"))
    return render_template("users/register.j2", register_form=register_form)


@blueprint.route("/settings", methods=["GET", "POST"])
def settings():
    return "settings"


def register_user(name, email, username, password, level, admin=False, send_email=True, **kwargs):
    new_user = User(name=name, username=username, password=password, email=email, level=level, admin=admin)
    for key, value in kwargs.items():
        setattr(new_user, key, value)
    code = random_string()
    new_user.email_token = code
    if send_email:
        send_verification_email(username, email, url_for("users.verify", code=code, _external=True))
    db.session.add(new_user)
    db.session.commit()
    return new_user


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
