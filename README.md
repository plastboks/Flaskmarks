Flask Bookmarks
===============

My simple and self educational Flask + sqlalchemy based bookmark app

Install
=======

Activate the virtualenv (ex: `. venv/bin/activate`)

make a copy of config.py.example to config.py and edit accordingly.

run `sh deploy.sh`

run `python db_create.py`

run `python db_migrate.py`

run `python db_upgrade.py`

then at last run `python run.py`


Deploy
======

make a copy of uwsgi.ini.example to uwsgi.ini and edit accordingly.

install uwsgi `pip install uwsgi` globally

copy flaskmarks.nginx.example to your nginx sites folder and enable

run `uwsgi uwsgi.ini`

restart nginx


Credits
=======

This app is heavily inspired by the flaks sqlalchemy tutorial @ http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


Useful Links
============
* http://pythonhosted.org/Flask-Principal/
* http://pythonhosted.org/Flask-SQLAlchemy/
