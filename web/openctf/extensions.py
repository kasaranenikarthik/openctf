from flask_cache import Cache
from flask_login import LoginManager
from celery import Celery

cache = Cache()
celery = None
login_manager = LoginManager()

login_manager.login_view = "users.login"
login_manager.login_message_category = "danger"


def make_celery(app):
    global celery
    celery = Celery(app.import_name, backend=app.config.get("CELERY_RESULT_BACKEND"), broker=app.config.get("CELERY_BROKER_URL"))
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
