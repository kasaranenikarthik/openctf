from datetime import datetime
from io import BytesIO

import requests
from Crypto.PublicKey import RSA
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

from openctf.extensions import login_manager
from openctf.util import generate_identicon

db = SQLAlchemy()


class Challenge(db.Model):
    __tablename__ = "challenges"
    id = db.Column(db.Integer, index=True, primary_key=True)
    author = db.Column(db.Unicode(32))
    name = db.Column(db.String(32), unique=True)
    title = db.Column(db.Unicode(64))
    description = db.Column(db.Text)
    hint = db.Column(db.Text)
    category = db.Column(db.Unicode(64))
    value = db.Column(db.Integer)

    grader = db.Column(db.UnicodeText)
    autogen = db.Column(db.Boolean)
    programming = db.Column(db.Boolean)
    threshold = db.Column(db.Integer)
    weightmap = db.Column(db.PickleType)

    solves = db.relationship("Solve", back_populates="challenge", lazy="subquery")

    def __repr__(self):
        return "Challenge:{}".format(self.id)


class Config(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Unicode(32), index=True)
    value = db.Column(db.Text)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @classmethod
    def get(cls, key, default=None):
        """ Get a single value from the configuration table. """
        config = cls.query.filter_by(key=key).first()
        if config is None:
            return default
        return config.value

    @classmethod
    def get_many(cls, keys):
        pairs = dict()
        configs = list(cls.query.all())
        for config in configs:
            if config.key in keys:
                pairs[config.key] = config.value
        return pairs

    @classmethod
    def set(cls, key, value):
        """ Set a value in the configuration table. """
        config = cls.query.filter_by(key=key).first()
        if config is None:
            config = Config(key, str(value))
        config.value = str(value)
        db.session.add(config)
        db.session.commit()

    @classmethod
    def set_many(cls, pairs):
        """ Sets many values in the configuration table. """
        for key, value in pairs.items():
            config = cls.query.filter_by(key=key).first()
            if config is None:
                config = Config(key, str(value))
            config.value = str(value)
            db.session.add(config)
        db.session.commit()

    @classmethod
    def get_ssh_keys(cls):
        pairs = cls.get_many(["private_key", "public_key"])
        private_key = pairs.get("private_key")
        public_key = pairs.get("public_key")
        if not (private_key and public_key):
            key = RSA.generate(2048)
            private_key = key.exportKey("PEM").decode("utf-8")
            public_key = key.publickey().exportKey("OpenSSH").decode("utf-8")
            cls.set_many(dict(
                private_key=private_key,
                public_key=public_key
            ))
        return private_key, public_key


class Solve(db.Model):
    __tablename__ = "solves"
    id = db.Column(db.Integer, index=True, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("challenges.id"), index=True)
    tid = db.Column(db.Integer, db.ForeignKey("teams.id"), index=True)
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    _date = db.Column("date", db.DateTime, default=datetime.utcnow)
    correct = db.Column(db.Boolean)
    flag = db.Column(db.Text)

    user = db.relationship("User", back_populates="solves", lazy="subquery")
    team = db.relationship("Team", back_populates="solves", lazy="subquery")
    challenge = db.relationship("Challenge", back_populates="solves", lazy="subquery")

    def __repr__(self):
        return "Solve:{}".format(self.id)


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, index=True, primary_key=True)
    teamname = db.Column(db.Unicode(32), unique=True)
    affiliation = db.Column(db.Unicode(48))
    captain = db.Column(db.Integer)
    banned = db.Column(db.Boolean)

    members = db.relationship("User", back_populates="team")
    solves = db.relationship("Solve", back_populates="team", lazy="subquery")

    def __repr__(self):
        return "Team:{}".format(self.id)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, index=True, primary_key=True)
    tid = db.Column(db.Integer, db.ForeignKey("teams.id"))
    name = db.Column(db.Unicode(32))
    username = db.Column(db.String(16), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    _password = db.Column("password", db.String(128))
    admin = db.Column(db.Boolean, default=False)
    level = db.Column(db.Integer)
    _register_time = db.Column("register_time", db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(32))
    otp_secret = db.Column(db.String(16))
    otp_confirmed = db.Column(db.Boolean, default=False)
    email_token = db.Column(db.String(32))
    email_verified = db.Column(db.Boolean, default=False)
    _avatar = db.Column("avatar", db.String(128))

    team = db.relationship("Team", back_populates="members")
    solves = db.relationship("Solve", back_populates="user", lazy="subquery")

    @property
    def avatar(self):
        if not self._avatar:
            avatar_file = BytesIO()
            avatar = generate_identicon(self.email)
            avatar.save(avatar_file, format="PNG")
            avatar_file.seek(0)
            response = requests.post("http://filestore:8000/save",
                                     data={"prefix": "avatar"},
                                     files={"file": avatar_file})
            if response.status_code == 200:
                self._avatar = "/static/%s" % response.text
                db.session.add(self)
                db.session.commit()
        return self._avatar

    def __repr__(self):
        return "User:{}".format(self.id)

    def check_password(self, password):
        """ Checks an unhashed password candidate against the stored password. """
        return bcrypt.verify(password, self.password)

    def get_id(self):
        """ Returns a string representation of the user's ID. """
        return str(self.id)

    @staticmethod
    @login_manager.user_loader
    def get_by_id(id):
        query_results = User.query.filter_by(id=id)
        return query_results.first()

    @property
    def is_active(self):
        # TODO This will be based off account standing.
        return True

    @property
    def is_authenticated(self):
        return True

    @hybrid_property
    def password(self):
        """ Returns the hashed password of the user. """
        return self._password

    @password.setter
    def password(self, password):
        """ Encrypts and sets the password. """
        self._password = bcrypt.encrypt(password, rounds=10)
