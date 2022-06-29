#!/usr/bin/env python
import os
from main_app import create_app, mysqldb
from main_app.database.model import User
from flask.ext.script import Manager, Shell
#from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
#migrate = Migrate(app, db)


def make_shell_context():
    return dict(app = app, db = mysqldb, User = User)
manager.add_command("shell", Shell(make_context = make_shell_context))
#manager.add_command('db', MigrateCommand)

'''
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
'''

if __name__ == '__main__':
    manager.run()
