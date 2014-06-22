from .setup import app
from datetime import datetime
from webhelpers2.date import time_ago_in_words
from hashlib import md5


@app.template_filter('date')
def _jinja2_filter_date(dateobj):
    return dateobj.strftime('%Y-%m-%d')


@app.template_filter('length')
def _jinja2_filter_date(list):
    return len(list)


@app.template_filter('tagsize')
def _jinja2_filter_date(list):
    size = (len(list))
    if size <= 1:
        size = 2
    return "style=font-size:%dpx" % (size * 5)


@app.template_filter('datetime')
def _jinja2_filter_datetime(dateobj):
    return dateobj.strftime('%Y-%m-%d %H:%M:%S')


@app.template_filter('datetimestr')
def _jinja2_filter_datetimestr(datetimestr):
    date_n_time = datetimestr.split('T')
    time = date_n_time[1].split('.')
    return date_n_time[0]+" "+time[0]


@app.template_filter('sectomin')
def _jinja_filter_sectomin(sec):
    return "%.2f" % (float(sec)/60)


@app.template_filter('thousandsep')
def _jinja_filter_sectomin(arg):
    return '{0:,}'.format(int(arg))


@app.template_filter('datewordsstr')
def _jinja2_filter_dateinwordsstr(datetimestr):
    date_n_time = datetimestr.split('T')
    time = date_n_time[1].split('.')
    date = date_n_time[0]+" "+time[0]
    dateobj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return time_ago_in_words(dateobj, round=True, granularity='day')


@app.template_filter('datewords')
def _jinja2_filter_dateinwords(dateobj):
    return time_ago_in_words(dateobj, round=True, granularity='day')


@app.template_filter('gravatar')
def _jinja_filter_gravatar(email):
    url = 'https://www.gravatar.com/avatar/'
    params = '?d=mm&s='+str(100)
    return url + md5(email).hexdigest() + params

@app.template_filter('enumerate')
def _jinja_filter_enumerate(list):
    return enumerate(list)

