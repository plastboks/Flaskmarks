# flaskmarks/core/setup.py

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.bootstrap import Bootstrap
from flask.ext.debugtoolbar import DebugToolbarExtension
from .. import app

app.config.from_object('config')
config = app.config

"""
Debug mode
"""
app.debug = config['DEBUG_MODE']

"""
Toolbar
"""
toolbar = DebugToolbarExtension(app)

"""
Login manager
"""
lm = LoginManager()
lm.init_app(app)

"""
Database ORM
"""
db = SQLAlchemy(app)

"""
DB migration
"""
migrate = Migrate(app, db)

"""
Manager
"""
manager = Manager(app)
manager.add_command('db', MigrateCommand)

"""
Bcrypt
"""
bcrypt = Bcrypt(app)

"""
Bootstrap
"""
Bootstrap(app)
