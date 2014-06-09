# @package flaskmarks
#
# @version 0.12
#
# @author Alexander Skjolden
#
# @date 2013-06-06
#


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
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

from flaskmarks import (
    viewsme,
    models,
    filters,
)

from .views.profile import profile
from .views.auth import auth
from .views.tags import tags
from .views.marks import marks
app.register_blueprint(profile)
app.register_blueprint(auth)
app.register_blueprint(tags)
app.register_blueprint(marks)
