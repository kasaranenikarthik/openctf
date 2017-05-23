from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import ValidationError
from wtforms.fields import *
from wtforms.validators import *

from openctf.config import get_require_email_verification
from openctf.models import User
from openctf.util import get_redirect_target, redirect_back

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
    return render_template("users/login.html", login_form=login_form, next=redirect_to)


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
    return render_template("users/profile.html", user=user)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    return "register"


@blueprint.route("/settings", methods=["GET", "POST"])
def settings():
    return "settings"


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
