# flaskmarks/views/profile.py

from flask import (
    Blueprint,
    render_template,
    g,
    flash,
    redirect,
    url_for,
)
from flask.ext.login import login_required
from ..core.setup import config, db, bcrypt
from ..forms import UserRegisterForm, UserProfileForm
from ..models import User

profile = Blueprint('profile', __name__)


@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def userprofile():
    u = g.user
    form = UserProfileForm(obj=u)
    """
    POST
    """
    if form.validate_on_submit():
        form.populate_obj(u)
        if form.password.data:
            u.password = bcrypt.generate_password_hash(form.password.data)
        else:
            del u.password
        db.session.add(u)
        db.session.commit()
        flash('User "%s" updated.' % (form.username.data), category='success')
        return redirect(url_for('profile.userprofile'))
    """
    GET
    """
    return render_template('profile/view.html',
                           form=form,
                           title='Profile',
                           bc=g.user.get_mark_count(),
                           fc=g.user.get_feed_count(),
                           lcm=g.user.mark_last_created()
                           )


@profile.route('/register', methods=['GET', 'POST'])
def register():
    if not config['CAN_REGISTER']:
        abort(403)
    form = UserRegisterForm()
    """
    POST
    """
    if form.validate_on_submit():
        u = User()
        form.populate_obj(u)
        u.password = bcrypt.generate_password_hash(form.password.data)
        try:
            db.session.add(u)
            db.session.commit()
            flash('New user "%s" registered.'
                  % (form.username.data), category='success')
            return redirect(url_for('auth.login'))
        except Exception as detail:
            flash('Problem registering "%s".'
                  % (form.username.data), category='danger')
    """
    GET
    """
    return render_template('profile/register.html',
                           form=form,
                           title='Register',
                           )
