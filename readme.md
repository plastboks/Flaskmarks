Flask Bookmarks
===============
My simple (and self educational) Flask + sqlalchemy based bookmark and RSS feed app.

Install
=======
* Activate the virtualenv (ex: `. venv/bin/activate`)
* make a copy of config.py.example to config.py and edit accordingly.
* run `pip install -r requirements.txt`
* run `python db_create.py`
* run `python db_migrate.py`
* run `python db_upgrade.py`
* run `python run.py`

Ubuntu
======
Installing this app on ubuntu may take a little more effort than `pip install -r requirements.txt`.
* run `sudo apt-get install python-virtualenv`
* run `sudo apt-get install python2.7-dev`
* run `sudo apt-get install build-essential`

Upgrade
=======
This is done by running: `python db_migrate && python db_upgrade`. 

Deploy
======
* make a copy of examples/uwsgi.ini.example to app root and edit accordingly.
* install uwsgi `pip install uwsgi` (globally?)
* copy examples/flaskmarks.nginx.example to your nginx sites folder and enable
* copy examples/uwsgi_params.example to your nginx config folder.
* run `uwsgi uwsgi.ini`
* restart nginx

Credits
=======
This app is heavily inspired by the flaks sqlalchemy tutorial @ http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world. Icons used in this app is mainly from the FamFamFam icon package 'Silk Icons' (http://www.famfamfam.com/lab/icons/silk/)

Branches
========
There will at any given point be at least two branches in this repository. One master (stable) branch, and one develop (unstable...) branch. The develop branch might contain unfinished code and/or wonky solutions for features. I will strive to make shure that code merged into master is as well thought of as possible (given the small size of this application).

Useful Links
============
* http://pythonhosted.org/Flask-Principal/
* http://pythonhosted.org/Flask-SQLAlchemy/
* http://jinja.pocoo.org/
* http://jinja.pocoo.org/docs/templates/#builtin-filters
* http://flask.pocoo.org/mailinglist/archive/2011/11/17/change-request-s-http-referer-header/#fc7dc5b7a1682ccbb4947a8013987761
