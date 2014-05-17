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

from flaskmarks import (
    views,
    models,
    filters,
)
