from flaskmarks import app
from datetime import datetime
from webhelpers2.date import time_ago_in_words
from hashlib import md5


@app.template_filter('date')
def _jinja2_filter_datetime(date):
    return date.strftime('%Y-%m-%d')


@app.template_filter('datewords')
def _jinja2_filter_dateinwords(date):
    return time_ago_in_words(date, round=True, granularity='day')

@app.template_filter('gravatar')
def _jinja_filter_gravatar(email):
    url = 'https://www.gravatar.com/avatar/'
    params = '?d=mm&s='+str(100)
    return  url + md5(email).hexdigest() + params
