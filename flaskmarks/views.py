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

from BeautifulSoup import BeautifulSoup as BSoup
from urllib import urlopen
from datetime import datetime
from urlparse import urlparse, urljoin

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
    BookmarkForm,
    UserRegisterForm,
    UserProfileForm,
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
    flash('Unauthorized access', category='error')
    return redirect(url_for('login'))


@app.errorhandler(403)
def forbidden(error):
    flash('Forbidden access', category='error')
    return redirect(url_for('index'))


#################
# Bookmark CRUD #
#################
@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
@login_required
def index(page = 1):
    u = g.user
    return render_template('index.html',
                            title = 'Home',
                            header = '',
                            bookmarks = u.bookmarks(page),
                            suggestions = u.suggestions(),
                            recently = u.recent())

@app.route('/bookmark/new', methods=['GET', 'POST'])
@login_required
def new_bookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        b = Bookmark()
        form.populate_obj(b)
        b.owner_id = g.user.id
        b.created = datetime.utcnow()
        b.tags = ' '.join(
                      [t.strip() for t in form.tags.data.strip().split(',')])\
                    .lower()
        b.clicks = 0
        if not form.title.data:
            soup = BSoup(urlopen(form.url.data))
            b.title = soup.title.string
        db.session.add(b)
        db.session.commit()
        flash('New bookmark %s added' % (b.title), category='info')
        return redirect(url_for('index'))
    return render_template('new.html',
                            title = 'New',
                            form = form)

@app.route('/bookmark/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(id):
    b = g.user.bid(id)
    form = BookmarkForm(obj=b)
    if not b:
        abort(403)
    if form.validate_on_submit():
        form.populate_obj(b)
        b.updated = datetime.utcnow()
        db.session.add(b)
        db.session.commit()
        flash('Bookmark %s updated' % (form.title.data), category='info')
        if form.referrer.data and is_safe_url(form.referrer.data):
          return redirect(form.referrer.data)
        return redirect(url_for('index'))
    form.referrer.data = request.referrer
    return render_template('edit.html',
                           title = 'Edit',
                           form = form)

@app.route('/bookmark/delete/<int:id>')
@login_required
def delete_bookmark(id):
    b = g.user.bid(id)
    if b:
        db.session.delete(b)
        db.session.commit()
        flash('Bookmark %s deleted' % (b.title), category='info')
        return redirect(url_for('index'))
    abort(403)


##################
# Search section #
##################
@app.route('/search/tag/<slug>')
@app.route('/search/tag/<slug>/<int:page>')
@login_required
def search_tags(slug, page = 1):
    b = g.user.btag(page, slug)
    return render_template('index.html',
                            title = 'Results',
                            header = 'Results for '+slug,
                            bookmarks = b)

@app.route('/search', methods=['GET'])
@app.route('/search/<int:page>', methods=['GET'])
@login_required
def search_string(page = 1):
    q = request.args.get('q')
    if not q:
        return redirect(url_for('index'))
    b = g.user.bstring(page, q)
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
    if request.args.get('id'):
        id = int(request.args.get('id'))
        b = g.user.bid(id)
        if b:
          if not b.clicks:
              b.clicks = 0;
          b.last_clicked = datetime.utcnow()
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
    bc = g.user.bookmark_count()
    lc = g.user.bookmark_last_created()
    form = UserProfileForm(obj=u)
    if form.validate_on_submit():
        form.populate_obj(u)
        if form.password.data:
            pm = bMan()
            u.password = pm.encode(form.password.data)
        else:
            del u.password
        db.session.add(u)
        db.session.commit()
        flash('User %s updated' % (form.username.data), category='info')
        return redirect(url_for('login'))
    return render_template('profile.html',
                            form = form,
                            title = 'Profile',
                            bc = bc,
                            lc = lc)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not app.config['CAN_REGISTER']:
        abort(403)
    form = UserRegisterForm()
    if form.validate_on_submit():
        u = User()
        pm = bMan()
        form.populate_obj(u)
        u.password = pm.encode(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('New user %s registered' % (form.username.data), category='info')
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
        u = User.by_uname_or_email(form.username.data)
        if u and u.authenticate_user(form.password.data):
            u.last_logged = datetime.utcnow()
            db.session.add(u)
            db.session.commit()
            flash('Successful login request for %s' % (u.username),\
                  category='info')
            login_user(u, remember = form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Failed login request for %s' % (form.username.data),\
                  category='error')
            return redirect(url_for('login'))
    return render_template('login.html',
                            title = 'Login',
                            form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#################
# Other Section #
#################
@app.route('/redirect/<int:id>')
@login_required
def bookmark_redirect(id):
    url = url_for('bookmark_meta', id=id)
    return render_template('meta.html', url=url)

@app.route('/meta/<int:id>')
@login_required
def bookmark_meta(id):
    b = g.user.bid(id)
    if b:
        return render_template('meta.html', url=b.url)
    abort(403)

# yanked from flask.pocoo.org/snippets/62
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
