# flaskmarks/views/auth.py

from flask import (
    Blueprint,
    render_template,
    g,
    flash,
    redirect,
    url_for,
)
from flask.ext.login import (
    login_required,
    login_user,
    logout_user
)
from datetime import datetime
from flaskmarks.core.setup import db
from flaskmarks.forms import LoginForm
from flaskmarks.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated():
        return redirect(url_for('marks.allmarks'))
    form = LoginForm()
    """
    POST
    """
    if form.validate_on_submit():
        u = User.by_uname_or_email(form.username.data)
        if u and u.authenticate_user(form.password.data):
            u.last_logged = datetime.utcnow()
            db.session.add(u)
            db.session.commit()
            flash('Welcome %s.' % (u.username),
                  category='info')
            login_user(u, remember=form.remember_me.data)
            return redirect(url_for('marks.allmarks'))
        else:
            flash('Failed login for %s.' % (form.username.data),
                  category='error')
            return redirect(url_for('auth.login'))
    """
    GET
    """
    return render_template('auth/login.html',
                           title='Login',
                           form=form,
                           )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


