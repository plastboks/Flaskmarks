from flask import (
    render_template,
    make_response,
    flash,
    redirect,
    session,
    url_for,
    g,
    request,
    current_app,
    abort,
    jsonify,
    json
)

from BeautifulSoup import BeautifulSoup as BSoup
from urllib import urlopen
from datetime import datetime
from urlparse import urlparse, urljoin
import feedparser

from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required,
)

from cryptacular.bcrypt import (
    BCRYPTPasswordManager as bMan,
)

from flaskmarks import (
    app,
    db,
    lm,
)

from forms import (
    LoginForm,
    MarkForm,
    UserRegisterForm,
    UserProfileForm,
    MarksImportForm
)

from models import (
    User,
    Mark,
    Tag,
    Meta
)


#################################
# Preloaders and error handlers #
#################################
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user

