# flaskmarks/core/error.py

from flask import flash, redirect, url_for, g, request
from flask.ext.login import current_user
from urlparse import urlparse, urljoin
from .setup import app, lm
from ..models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(401)
def unauthorized(error):
    if request.referrer \
        and is_safe_url(request.referrer) \
            and request.referrer is not "/":
        flash('Unauthorized access.', category='error')
    return redirect(url_for('auth.login'))


@app.errorhandler(403)
def forbidden(error):
    flash('Forbidden access.', category='error')
    return redirect(url_for('marks.allmarks'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and\
        ref_url.netloc == test_url.netloc
