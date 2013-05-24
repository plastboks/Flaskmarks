from flask import (
    render_template,
    flash,
    redirect,
    session,
    url_for,
    g,
    request,
    current_app,
    abort,
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
    NewBookmarkForm,
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


@app.errorhandler(403)
def forbidden(error):
    flash('Forbidden access')
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    u = g.user
    b = Bookmark.my_bookmarks(u.id)
    return render_template('index.html',
                            title = 'Home',
                            user = u,
                            bookmarks = b)


@app.route('/bookmark/new', methods=['GET', 'POST'])
@login_required
def new_bookmark():
    form = NewBookmarkForm()
    if form.validate_on_submit():
        u = g.user
        b = Bookmark()
        form.populate_obj(b)
        b.owner_id = u.id
        db.session.add(b)
        db.session.commit()
        flash('New bookmark %s added' % (form.title.data))
        return redirect(url_for('index'))
    return render_template('new.html',
                            title = 'New',
                            form = form)


@app.route('/bookmark/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(id):
    u = g.user
    b = Bookmark.by_id(u.id, id) 
    form = NewBookmarkForm(obj=b)
    if not b:
        abort(403)
    if form.validate_on_submit():
        form.populate_obj(b)
        db.session.add(b)
        db.session.commit()
        flash('Bookmark %s updated' % (form.title.data))
        return redirect(url_for('index'))
    return render_template('edit.html',
                           title = 'Edit',
                           form = form)


@app.route('/bookmark/delete/<int:id>')
@login_required
def delete_bookmark(id):
    u = g.user
    b = Bookmark.by_id(u.id, id) 
    if b:
        db.session.delete(b)
        db.session.commit()
        flash('Bookmark %s deleted' % (b.title))
        return redirect(url_for('index'))
    abort(403)


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
        return redirect(url_for('login'))
    return render_template('register.html',
                            form = form,
                            title = 'Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated():
        return redirect(url_for('index'))
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
    return redirect(url_for('login'))
