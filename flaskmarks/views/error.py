# flaskmarks/views/error.py

from flask import (
    Blueprint,
    render_template,
    g,
    flash,
    redirect,
    url_for,
)

from flaskmarks.core.setup import db
from flaskmarks.core.error import is_safe_url
from urlparse import urlparse, urljoin

error = Blueprint('error', __name__)

@error.errorhandler(401)
def unauthorized(error):
    if request.referrer \
        and is_safe_url(request.referrer) \
            and request.referrer is not "/":
        flash('Unauthorized access.', category='error')
    return redirect(url_for('login'))


@error.errorhandler(403)
def forbidden(error):
    flash('Forbidden access.', category='error')
    return redirect(url_for('marks'))
