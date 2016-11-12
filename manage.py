#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """
    Make the shell context
    """
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host='0.0.0.0'))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
