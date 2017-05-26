import os
import pathlib
import sys

from openctf.extensions import cache
from openctf.util import random_string
from openctf.models import Config as _Config


class Config(object):
    def __init__(self, app_root=None):
        environment = os.getenv("ENVIRONMENT", "development")

        if app_root is None:
            self.app_root = pathlib.Path(
                os.path.dirname(os.path.abspath(__file__)))
        else:
            self.app_root = pathlib.Path(app_root)

        self.CACHE_TYPE = "redis"
        self.CACHE_REDIS_HOST = "redis"

        self.CELERY_BROKER_URL = "redis://redis:6379/0"
        self.CELERY_RESULT_BACKEND = "redis://redis:6379/0"

        self.SECRET_KEY = self._get_secret_key()
        self.SQLALCHEMY_DATABASE_URI = Config.get_database_url()
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True

        if environment == "development":
            self.TEMPLATES_AUTO_RELOAD = True

    def _get_secret_key(self):
        if "SECRET_KEY" in os.environ:
            return os.environ["SECRET_KEY"]
        else:
            secret_path = self.app_root / ".secret_key"
            if not os.path.exists(secret_path):
                open(secret_path, "w").close()
            with secret_path.open("rb+") as secret_file:
                secret_file.seek(0)
                contents = secret_file.read()
                if not contents and len(contents) == 0:
                    key = os.urandom(128)
                    secret_file.write(key)
                    secret_file.flush()
                else:
                    key = contents
        return key

    @staticmethod
    def get_database_url():
        url = os.getenv("DATABASE_URL")
        if url:
            return url
        user = os.getenv("DB_USER")
        passwd = os.getenv("MYSQL_ROOT_PASSWORD")
        host = os.getenv("DB_HOST")
        port = int(os.getenv("DB_PORT", "3306"))
        name = os.getenv("DB_NAME")
        if user and passwd and host and port and name:
            fmt = dict(user=user, passwd=passwd, host=host, port=port, name=name)
            return "mysql://{user}:{passwd}@{host}:{port}/{name}".format(**fmt)
        sys.stderr.write("No database URL specified. Please check your configuration!\n")
        sys.stderr.flush()
        sys.exit(1)


def generate_verification_token():
    token = random_string()
    sys.stdout.write("Your CTF verification token is: {}\n".format(token))
    sys.stdout.flush()
    _Config.set("setup_verification", value=token)


@cache.memoize()
def setup_complete():
    value = _Config.get("setup_complete")
    return bool(value)


@cache.memoize()
def get_ctf_name():
    return _Config.get("ctf_name", "OpenCTF")


@cache.memoize()
def get_require_email_verification():
    value = _Config.get("require_email_verification", 0)
    return bool(int(value))


@cache.memoize()
def get_allow_registrations():
    value = _Config.get("allow_registrations", 0)
    return bool(int(value))
