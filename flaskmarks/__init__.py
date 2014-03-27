## @package flaskmarks
#
# @version 0.12
#
# @author Alexander Skjolden
#
# @date 2013-06-06
#


from flask import Flask
from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

cache = Cache()
app = Flask(__name__)
cache.init_app(app, config={'CACHE_TYPE': 'null'})
app.config.from_object('config')
config = app.config
lm = LoginManager()
lm.init_app(app)
db = SQLAlchemy(app)

from flaskmarks import (
    views,
    models,
    filters,
)
