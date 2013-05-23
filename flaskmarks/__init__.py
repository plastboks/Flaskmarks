from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.principal import Principal

app = Flask(__name__)
app.config.from_object('config')
Principal(app)
lm = LoginManager()
lm.init_app(app)
db = SQLAlchemy(app)


from flaskmarks import views, models
