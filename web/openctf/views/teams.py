from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from openctf.models import db, Activity, Team

blueprint = Blueprint("teams", __name__, template_folder="templates")


@blueprint.route("/create", methods=["GET", "POST"])
def create():
    if current_user.tid:
        return redirect(url_for("teams.profile"))
    create_team_form = CreateTeamForm(prefix="create")
    if create_team_form.validate_on_submit():
        create_team(create_team_form)
        return redirect(url_for("teams.profile"))
    return render_template("teams/create.j2", create_team_form=create_team_form)


@blueprint.route("/profile", methods=["GET", "POST"])
@blueprint.route("/profile/<int:tid>", methods=["GET", "POST"])
def profile(tid=None):
    return "profile"


def create_team(form):
    new_team = Team(captain=current_user.id)
    db.session.add(new_team)
    db.session.commit()
    current_user.tid = new_team.id
    form.populate_obj(current_user.team)
    db.session.add(current_user)
    db.session.commit()

    activity = Activity(uid=current_user.id, tid=new_team.id, _type=Activity.CREATED_TEAM)
    db.session.add(activity)
    db.session.commit()
    return new_team


class CreateTeamForm(FlaskForm):
    teamname = StringField("Team Name", validators=[
        InputRequired("Please enter a team name."),
        Length(3, 24,
               "Your teamname must be between 3 and 24 characters long.")])
    affiliation = StringField("Affiliation", validators=[
        InputRequired("Please enter your school."),
        Length(3, 36,
               "Your school name must be between 3 and 36 characters long." +
               "Use abbreviations if necessary.")])
    submit = SubmitField("Create Team")

    def validate_teamname(self, field):
        if current_user.tid is not None:
            raise ValidationError("You are already in a team.")
        if Team.query.filter(
                func.lower(Team.teamname) == field.data.lower()).count():
            raise ValidationError("Team name is taken.")
