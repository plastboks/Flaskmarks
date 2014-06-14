# flaskmarks/core/blueprints.py

from .setup import app

from ..views import (
    profile,
    auth,
    tags,
    marks
)
app.register_blueprint(profile.profile)
app.register_blueprint(auth.auth)
app.register_blueprint(tags.tags)
app.register_blueprint(marks.marks)
