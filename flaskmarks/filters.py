from flaskmarks import app
from datetime import datetime
from webhelpers2.date import time_ago_in_words


@app.template_filter('date')
def _jinja2_filter_datetime(date):
    return date.strftime('%Y-%m-%d')


@app.template_filter('datewords')
def _jinja2_filter_dateinwords(date):
    return time_ago_in_words(date, round=True, granularity='day')
