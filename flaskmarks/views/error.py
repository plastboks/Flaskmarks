# flaskmarks/views/error.py

from flask import (
    Blueprint,
    render_template,
    g,
    flash,
    redirect,
    url_for,
)

from flaskmarks import db
from urlparse import urlparse, urljoin

error = Blueprint('error', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and\
        ref_url.netloc == test_url.netloc

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


