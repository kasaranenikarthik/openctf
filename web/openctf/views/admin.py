from datetime import datetime
import string

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import *
from wtforms.validators import *
from wtforms_components import read_only

from openctf.config import (get_allow_registrations, get_ctf_name,
                            get_require_email_verification)
from openctf.extensions import cache
from openctf.decorators import admin_required
from openctf.models import Config
from openctf.util import RequiredIf

blueprint = Blueprint("admin", __name__, template_folder="templates")


@blueprint.route("/")
@admin_required
def index():
    return "overview"


@blueprint.route("/settings", methods=["GET", "POST"])
@admin_required
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
        cache.delete_memoized(get_ctf_name)
        cache.delete_memoized(get_allow_registrations)
        cache.delete_memoized(get_require_email_verification)
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
            else:
                keys.append(field.short_name)
        pairs = Config.get_many(keys)
        for field in settings_form:
            if field.short_name in ["csrf_token", "public_key"]:
                continue
            data = pairs.get(field.short_name)
            if field.short_name in ["allow_registrations", "require_email_verification"]:
                field.data = int(data)
            elif field.short_name in ["start_time", "end_time"] and data:
                field.data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
            else:
                field.data = data
    return render_template("admin/settings.j2", settings_form=settings_form)


class SettingsForm(FlaskForm):
    ctf_name = StringField("CTF Name", validators=[InputRequired("Please enter a CTF name.")])
    ctf_description = TextAreaField("CTF Description", validators=[])
    team_size = IntegerField("Team Size", default=5, validators=[NumberRange(min=1), InputRequired("Please enter a max team size.")])

    allow_registrations = BooleanField("Allow Registrations")
    require_email_verification = BooleanField("Require email verification")
    mailgun_email = TextField("Mailgun Email", validators=[RequiredIf("require_email_verification")])
    mailgun_domain = TextField("Mailgun Domain", validators=[RequiredIf("require_email_verification")])
    mailgun_apikey = TextField("Mailgun API Key", validators=[RequiredIf("require_email_verification")])
    email_body = TextAreaField("Email Body", validators=[RequiredIf("require_email_verification")])

    start_time = DateTimeField("Start Time", validators=[InputRequired("Please enter a CTF start time.")])
    end_time = DateTimeField("End Time", validators=[InputRequired("Please enter a CTF end time.")])

    webhook_secret = StringField("Webhook Secret", validators=[Optional()])
    public_key = StringField("Public Key", validators=[Optional()])

    keywords = StringField("Keywords", validators=[Optional()])
    submit = SubmitField("Save Settings")

    def validate_email_body(self, field):
        try:
            string.Template(field.data).substitute(
                ctf_name="test",
                link="test",
                username="test",
            )
        except:
            raise ValidationError("Bad email template.")
