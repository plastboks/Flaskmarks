from flaskmarks import app
from datetime import datetime
from flask.ext.gravatar import Gravatar
from webhelpers2.date import time_ago_in_words


@app.template_filter('date')
def _jinja2_filter_datetime(date):
    return date.strftime('%Y-%m-%d')


@app.template_filter('datewords')
def _jinja2_filter_dateinwords(date):
    return time_ago_in_words(date, round=True, granularity='day')

@app.template_filter('gravatar')
def _jinja_filter_gravatar(size = False, rating = False):
    gravatar = Gravatar(app,
                     size=100,
                     rating='r',
                     default='retro',
                     force_default=False,
                     force_lower=False,
                     use_ssl=True,
                     base_url=None)
    return gravatar
