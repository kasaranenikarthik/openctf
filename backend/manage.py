#!/usr/bin/env python3

import os

from celery.bin.celery import main as celery_main
from flask_migrate import Migrate, MigrateCommand
from flask_script import Command, Manager, Server

from openctf import create_app
from openctf.models import db

app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

port = int(os.getenv("OPENCTF_PORT", "80"))
ServerCommand = Server(host="0.0.0.0", port=port, use_debugger=False, use_reloader=True)
manager.add_command("runserver", ServerCommand)


class CeleryCommand(Command):
    def run(self):
        celery_args = ["celery", "worker", "-C", "--autoscale=10,1", "--without-gossip"]
        with app.app_context():
            return celery_main(celery_args)


manager.add_command("worker", CeleryCommand())

if __name__ == "__main__":
    manager.run()
