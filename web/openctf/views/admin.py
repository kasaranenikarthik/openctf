from flask import Blueprint, flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import *
from wtforms.validators import *
from wtforms_components import read_only

from openctf.models import Config

blueprint = Blueprint("admin", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    return "overview"


@blueprint.route("/settings", methods=["GET", "POST"])
def settings():
    settings_form = SettingsForm()
    read_only(settings_form.public_key)
    if settings_form.validate_on_submit():
        pairs = dict()
        for field in settings_form:
            if field.short_name in ["csrf_token", "public_key", "submit"]:
                continue
            data = field.data
            if type(data) == bool:
                data = int(data)
            pairs[field.short_name] = data
        Config.set_many(pairs)
        flash("Settings saved!", "success")
        return redirect(url_for("admin.settings"))
    else:
        keys = []
        for field in settings_form:
            if field.short_name == "csrf_token":
                continue
            if field.short_name == "public_key":
                private_key, public_key = Config.get_ssh_keys()
                field.data = public_key
                continue
            keys.append(field.short_name)
        pairs = Config.get_many(keys)
        for field in settings_form:
            if field.short_name in ["csrf_token", "public_key"]:
                continue
            if field.short_name in ["allow_registrations"]:
                field.data = int(pairs.get(field.short_name))
                continue
            field.data = pairs.get(field.short_name)
    return render_template("admin/settings.html", settings_form=settings_form)


class SettingsForm(FlaskForm):
    ctf_name = StringField("CTF Name", validators=[InputRequired("Please enter a CTF name.")])
    ctf_description = TextAreaField("CTF Description", validators=[])
    team_size = IntegerField("Team Size", default=5, validators=[NumberRange(min=1), InputRequired("Please enter a max team size.")])

    allow_registrations = BooleanField("Allow Registrations")
    require_email_verification = BooleanField("Require email verification")
    mailgun_domain = TextField("Mailgun Domain", validators=[])

    start_time = IntegerField("Start Time", validators=[InputRequired("Please enter a CTF start time.")])
    end_time = IntegerField("End Time", validators=[InputRequired("Please enter a CTF end time.")])

    webhook_secret = StringField("Webhook Secret", validators=[Optional()])
    public_key = StringField("Public Key", validators=[Optional()])

    keywords = StringField("Keywords", validators=[Optional()])
    submit = SubmitField("Save Settings")
