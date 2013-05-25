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
    jsonify,
    )

from datetime import datetime

from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required,
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
    UserForm,
    BookmarkForm,
    )

from models import (
    User,
    Bookmark,
    )


################################
# Preloaders and errorhandlers #
################################
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


#################
# Bookmark CRUD #
#################
@app.route('/')
@app.route('/index')
@login_required
def index():
    u = g.user
    b = Bookmark.my_bookmarks(u.id)
    return render_template('index.html',
                            title = 'Home',
                            user = u,
                            header = 'My bookmarks',
                            bookmarks = b)

@app.route('/bookmark/new', methods=['GET', 'POST'])
@login_required
def new_bookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        u = g.user
        b = Bookmark()
        form.populate_obj(b)
        b.owner_id = u.id
        b.created = datetime.utcnow()
        b.tags = ' '.join(
                      [t.strip() for t in form.tags.data.strip().split(',')])\
                    .lower()
        b.clicks = 0
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
    form = BookmarkForm(obj=b)
    if not b:
        abort(403)
    if form.validate_on_submit():
        form.populate_obj(b)
        b.updated = datetime.utcnow()
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


##################
# Search section #
##################
@app.route('/search/tag/<slug>')
@login_required
def search_tags(slug):
    u = g.user
    b = Bookmark.by_tag(u.id, slug)
    return render_template('index.html',
                            title = 'Results',
                            header = 'Results for '+slug,
                            bookmarks = b)

@app.route('/search', methods=['GET'])
@login_required
def search_string():
    u = g.user
    q = request.args['q']
    if not q:
        return redirect(url_for('index'))
    b = Bookmark.by_string(u.id, q)
    return render_template('index.html',
                            title = 'Results',
                            header = 'Results for '+q,
                            bookmarks = b)

################
# AJAX section #
################
@app.route('/bookmark/inc')
@login_required
def ajax_bookmark_inc():
    u = g.user
    if request.args.get('id'):
        id = int(request.args.get('id'))
        b = Bookmark.by_id(u.id, id)
        if b:
          if not b.clicks:
              b.clicks = 0;
          b.clicks += 1
          db.session.add(b)
          db.session.commit()
          return jsonify(status='success')
        return jsonify(status='forbidden')
    return jsonify(status='error')


################
# User section #
################
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    u = g.user
    form = UserForm(obj=u)
    if form.validate_on_submit():
        pm = bMan()
        form.populate_obj(u)
        u.password = pm.encode(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('User %s updated' % (form.username.data))
        return redirect(url_for('login'))
    return render_template('profile.html',
                            form = form,
                            title = 'Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
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


########################
# Login/logout section #
########################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.by_username(form.username.data)
        if u and u.authenticate_user(form.password.data):
            u.last_logged = datetime.utcnow()
            db.session.add(u)
            db.session.commit()
            flash('Successful login request for %s' % (form.username.data))
            login_user(u)
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
    return redirect(url_for('login'))

