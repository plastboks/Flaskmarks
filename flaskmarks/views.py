from flask import (
    render_template,
    flash,
    redirect,
    session,
    url_for,
    g,
    request,
    current_app,
    )

from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    )

from flask.ext.principal import (
    Principal,
    Identity,
    AnonymousIdentity,
    identity_changed,
    )

from cryptacular.bcrypt import (
    BCRYPTPasswordManager as bMan,
    )
from flaskmarks import (
    app,
    db,
    lm,
    )

from forms import (
    LoginForm,
    RegisterForm,
    )

from models import (
    User,
    Bookmark,
    )


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.errorhandler(401)
def unauthorized(error):
    flash('Unauthorized access')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template('index.html',
        title = 'Home',
        user = user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User()
        pm = bMan()
        form.populate_obj(u)
        u.password = pm.encode(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('New user %s registered' % (form.username.data))
        return redirect(url_for('index'))
    return render_template('register.html',
                           form = form,
                           title = 'Register')


@app.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    if form.validate_on_submit():
        u = User.by_username(form.username.data)
        if u and u.authenticate_user(form.password.data):
            flash('Successful login request for %s' % (form.username.data))
            login_user(u)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(u.id))
            return redirect(url_for('index'))
        else:
            flash('Failed login request for %s' % (form.username.data))
            return redirect(url_for('login'))
    return render_template('login.html',
                           title = 'Login',
                           form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('index'))
