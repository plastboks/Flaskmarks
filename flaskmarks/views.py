from flask import (
    render_template,
    make_response,
    flash,
    redirect,
    session,
    url_for,
    g,
    request,
    current_app,
    abort,
    jsonify,
    json
)

from BeautifulSoup import BeautifulSoup as BSoup
from urllib import urlopen
from datetime import datetime
from urlparse import urlparse, urljoin
import feedparser

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
    MarkForm,
    UserRegisterForm,
    UserProfileForm,
    MarksImportForm
)

from models import (
    User,
    Mark,
    Tag,
    Meta
)


#################################
# Preloaders and error handlers #
#################################
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(401)
def unauthorized(error):
    if request.referrer \
        and is_safe_url(request.referrer) \
            and request.referrer is not "/":
        flash('Unauthorized access.', category='error')
    return redirect(url_for('login'))


@app.errorhandler(403)
def forbidden(error):
    flash('Forbidden access.', category='error')
    return redirect(url_for('marks'))


#############
# Mark CRUD #
#############
@app.route('/')
@app.route('/index')
def webroot():
    return redirect(url_for('marks'))


@app.route('/marks')
@app.route('/marks/<int:page>')
@login_required
def marks(page=1):
    u = g.user
    return render_template('mark/index.html',
                           title='Marks - page %d' % page,
                           header='',
                           marks=u.marks(page))


@app.route('/clicked')
@app.route('/clicked/<int:page>')
@login_required
def recently_clicked(page=1):
    u = g.user
    return render_template('mark/index.html',
                           title='Marks - page %d' % page,
                           header='',
                           marks=u.recent_marks(page, 'clicked'))


@app.route('/recently')
@app.route('/recently/<int:page>')
@login_required
def recently_added(page=1):
    u = g.user
    return render_template('mark/index.html',
                           title='Marks - page %d' % page,
                           header='',
                           marks=u.recent_marks(page, 'added'))


@app.route('/mark/new', methods=['GET', 'POST'])
@login_required
def new_mark():
    form = MarkForm()
    """
    POST
    """
    if form.validate_on_submit():
        if g.user.q_marks_by_url(form.url.data):
            flash('Mark with this url "%s" already\
                  exists.' % (form.url.data), category='error')
            return redirect(url_for('marks'))
        m = Mark()
        form.populate_obj(m)
        m.owner_id = g.user.id
        m.created = datetime.utcnow()
        m.clicks = 0

        """ Meta test area """
        clicks = Meta('clicks', 0)
        db.session.add(clicks)
        m.metas = [clicks]

        if not form.title.data:
            soup = BSoup(urlopen(form.url.data))
            m.title = soup.title.string
        db.session.add(m)
        db.session.commit()
        flash('New mark: "%s", added.' % (m.title), category='info')
        return redirect(url_for('marks'))
    """
    GET
    """
    if request.args.get('url'):
        form.url.data = request.args.get('url')
    if request.args.get('title'):
        form.title.data = request.args.get('title')
    if request.args.get('type') == 'feed':
        form.type.data = 'feed'
    return render_template('mark/new.html',
                           title='New mark',
                           form=form)


@app.route('/mark/view/<int:id>', methods=['GET'])
@login_required
def view_mark(id):
    m = g.user.get_mark_by_id(id)
    if not m:
        abort(403)
    if m.type != 'feed':
        abort(404)
    data = feedparser.parse(m.url)
    if m:
        if not m.clicks:
            m.clicks = 0
        m.last_clicked = datetime.utcnow()
        m.clicks += 1
        db.session.add(m)
        db.session.commit()
    return render_template('mark/view.html',
                           mark=m,
                           data=data,
                           title=m.title,
                           )


@app.route('/mark/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mark(id):
    m = g.user.get_mark_by_id(id)
    form = MarkForm(obj=m)
    if not m:
        abort(403)
    """
    POST
    """
    if form.validate_on_submit():
        if m.url != form.url.data and g.user.q_marks_by_url(form.url.data):
            flash('Mark with this url (%s) already\
                  exists.' % (form.url.data), category='error')
            return redirect(url_for('marks'))
        form.populate_obj(m)
        m.updated = datetime.utcnow()
        db.session.add(m)
        db.session.commit()
        flash('Mark "%s" updated.' % (form.title.data), category='info')
        if form.referrer.data and is_safe_url(form.referrer.data):
            return redirect(form.referrer.data)
        return redirect(url_for('marks'))
    """
    GET
    """
    form.referrer.data = request.referrer
    return render_template('mark/edit.html',
                           mark=m,
                           title='Edit mark - %s' % m.title,
                           form=form
                           )


@app.route('/mark/delete/<int:id>')
@login_required
def delete_mark(id):
    m = g.user.get_mark_by_id(id)
    if m:
        db.session.delete(m)
        db.session.commit()
        flash('Mark "%s" deleted.' % (m.title), category='info')
        """
        if request.referrer and is_safe_url(request.referrer):
            return redirect(request.referrer)
        """
        return redirect(url_for('marks'))
    abort(403)


################
# Tags section #
################
@app.route('/tagcloud', methods=['GET'])
@login_required
def tagcloud():
    return render_template('tag/cloud.html',
                           title='Tag cloud',
                           header='',
                           tags=g.user.all_tags())


@app.route('/tagsbyclicks', methods=['GET'])
@app.route('/tagbyclicks/<int:page>')
@login_required
def tags_by_click(page=1):
    u = g.user
    return render_template('tag/index.html',
                           title='Tags - page %d' % page,
                           header='',
                           tags=u.tags_by_click(page))


##################
# Search section #
##################
@app.route('/mark/tag/<slug>')
@app.route('/mark/tag/<slug>/<int:page>')
@login_required
def mark_q_tag(slug, page=1):
    return render_template('mark/index.html',
                           title='Marks with tag: %s' % (slug),
                           header='Marks with tag: %s' % (slug),
                           marks=g.user.q_marks_by_tag(slug, page))


@app.route('/search', methods=['GET'])
@app.route('/search/<int:page>', methods=['GET'])
@login_required
def search_string(page=1):
    q = request.args.get('q')
    t = request.args.get('type')

    if not q and not t:
        return redirect(url_for('marks'))

    m = g.user.q_marks_by_string(page, q, t)
    return render_template('mark/index.html',
                           title='Search results for: %s' % (q),
                           header="Search results for: '%s'" % (q),
                           marks=m)


################
# AJAX section #
################
@app.route('/mark/inc')
@login_required
def ajax_mark_inc():
    if request.args.get('id'):
        id = int(request.args.get('id'))
        m = g.user.get_mark_by_id(id)
        if m:
            if not m.clicks:
                m.clicks = 0
            m.last_clicked = datetime.utcnow()
            m.clicks += 1
            db.session.add(m)
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
    form = UserProfileForm(obj=u)
    """
    POST
    """
    if form.validate_on_submit():
        form.populate_obj(u)
        if form.password.data:
            pm = bMan()
            u.password = pm.encode(form.password.data)
        else:
            del u.password
        db.session.add(u)
        db.session.commit()
        flash('User "%s" updated.' % (form.username.data), category='info')
        return redirect(url_for('profile'))
    """
    GET
    """
    return render_template('account/profile.html',
                           form=form,
                           title='Profile',
                           bc=g.user.get_mark_count(),
                           fc=g.user.get_feed_count(),
                           lcm=g.user.mark_last_created()
                           )


@app.route('/marks/export.json', methods=['GET'])
@login_required
def export_marks():
    u = g.user
    d = [{'title': m.title,
          'type': m.type,
          'url': m.url,
          'clicks': m.clicks,
          'created': m.created.strftime('%s'),
          'updated': m.updated.strftime('%s') if m.updated else '',
          'last_clicked': m.last_clicked.strftime('%s') if m.last_clicked else '',
          'tags': [t.title for t in m.tags],
          'metas': [meta.name for meta in m.metas]}
         for m in u.all_marks()]
    return jsonify(marks=d)


@app.route('/marks/import', methods=['GET', 'POST'])
@login_required
def import_marks():
    u = g.user
    form = MarksImportForm(obj=u)
    """
    POST
    """
    if form.validate_on_submit():
        try:
            data = json.loads(form.file.data.read())
        except Exception as detail:
            flash('%s' % (detail), category='error')
            return redirect(url_for('profile'))
        count = 0
        for c in data['marks']:
            m = Mark()
            m.insert_from_import(u.id, c)
            count += 1
            db.session.add(m)
            db.session.commit()
        flash('%s marks imported' % (count), category='info')
        return redirect(url_for('profile'))
    """
    GET
    """
    return render_template('account/import.html',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not app.config['CAN_REGISTER']:
        abort(403)
    form = UserRegisterForm()
    """
    POST
    """
    if form.validate_on_submit():
        u = User()
        pm = bMan()
        form.populate_obj(u)
        u.password = pm.encode(form.password.data)
        try:
            db.session.add(u)
            db.session.commit()
            flash('New user "%s" registered.'
                  % (form.username.data), category='info')
            return redirect(url_for('login'))
        except Exception as detail:
            flash('Problem registering "%s".'
                  % (form.username.data), category='error')
    """
    GET
    """
    return render_template('account/register.html',
                           form=form,
                           title='Register',
                           )


########################
# Login/logout section #
########################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated():
        return redirect(url_for('marks'))
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
            return redirect(url_for('marks'))
        else:
            flash('Failed login for %s.' % (form.username.data),
                  category='error')
            return redirect(url_for('login'))
    """
    GET
    """
    return render_template('account/login.html',
                           title='Login',
                           form=form,
                           )


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
def mark_redirect(id):
    url = url_for('mark_meta', id=id)
    return render_template('meta.html', url=url)


@app.route('/meta/<int:id>')
@login_required
def mark_meta(id):
    b = g.user.bid(id)
    if b:
        return render_template('meta.html', url=b.url)
    abort(403)


# yanked from flask.pocoo.org/snippets/62
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and\
        ref_url.netloc == test_url.netloc
