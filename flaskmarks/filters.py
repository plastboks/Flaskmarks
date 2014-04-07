from flaskmarks import app
from datetime import datetime
from webhelpers2.date import time_ago_in_words
from hashlib import md5


@app.template_filter('date')
def _jinja2_filter_date(dateobj):
    return dateobj.strftime('%Y-%m-%d')

@app.template_filter('datetime')
def _jinja2_filter_datetime(dateobj):
    return dateobj.strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('datetimestr')
def _jinja2_filter_datetimestr(datetimestr):
    date_n_time = datetimestr.split('T')
    time = date_n_time[1].split('.')
    return date_n_time[0]+" "+time[0]


@app.template_filter('datewords')
def _jinja2_filter_dateinwords(dateobj):
    return time_ago_in_words(dateobj, round=True, granularity='day')

@app.template_filter('gravatar')
def _jinja_filter_gravatar(email):
    url = 'https://www.gravatar.com/avatar/'
    params = '?d=mm&s='+str(100)
    return  url + md5(email).hexdigest() + params
