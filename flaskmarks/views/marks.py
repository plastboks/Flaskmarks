# flaskmarks/views/profile.py

from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    g,
    request,
    abort,
    jsonify,
    json
)
from flask.ext.login import login_user, logout_user, login_required

from BeautifulSoup import BeautifulSoup as BSoup
from urllib import urlopen
from datetime import datetime
from urlparse import urlparse, urljoin
import feedparser

from ..core.setup import app, db
from ..core.error import is_safe_url
from ..forms import (
    LoginForm,
    MarkForm,
    MarkEditForm,
    UserRegisterForm,
    UserProfileForm,
    MarksImportForm
)
from ..models import User, Mark, Tag, Meta

marks = Blueprint('marks', __name__)


@marks.route('/')
@marks.route('/index')
def webroot():
    return redirect(url_for('marks.allmarks'))


@marks.route('/marks/all')
@marks.route('/marks/all/<int:page>')
@login_required
def allmarks(page=1):
    u = g.user
    return render_template('mark/index.html',
                           title='Marks - page %d' % page,
                           header='',
                           marks=u.marks(page))


@marks.route('/marks/sort/clicked')
@marks.route('/marks/sort/clicked/<int:page>')
@login_required
def recently_clicked(page=1):
    u = g.user
    return render_template('mark/index.html',
                           title='Marks - page %d' % page,
                           header='',
                           marks=u.recent_marks(page, 'clicked'))


@marks.route('/marks/sort/recently')
@marks.route('/marks/sort/recently/<int:page>')
@login_required
def recently_added(page=1):
    u = g.user
    return render_template('mark/index.html',
                           title='Marks - page %d' % page,
                           header='',
                           marks=u.recent_marks(page, 'added'))


@marks.route('/marks/search/tag/<slug>')
@marks.route('/marks/search/tag/<slug>/<int:page>')
@login_required
def mark_q_tag(slug, page=1):
    return render_template('mark/index.html',
                           title='Marks with tag: %s' % (slug),
                           header='Marks with tag: %s' % (slug),
                           marks=g.user.q_marks_by_tag(slug, page))


@marks.route('/marks/search/string', methods=['GET'])
@marks.route('/marks/search/string/<int:page>', methods=['GET'])
@login_required
def search_string(page=1):
    q = request.args.get('q')
    t = request.args.get('type')

    if not q and not t:
        return redirect(url_for('marks.allmarks'))

    m = g.user.q_marks_by_string(page, q, t)
    return render_template('mark/index.html',
                           title='Search results for: %s' % (q),
                           header="Search results for: '%s'" % (q),
                           marks=m)


@marks.route('/mark/new', methods=['GET', 'POST'])
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
            return redirect(url_for('marks.allmarks'))
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
        return redirect(url_for('marks.allmarks'))
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


@marks.route('/mark/view/<int:id>', methods=['GET'])
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


@marks.route('/mark/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mark(id):
    m = g.user.get_mark_by_id(id)
    form = MarkEditForm(obj=m)
    if not m:
        abort(403)
    """
    POST
    """
    if form.validate_on_submit():
        if m.url != form.url.data and g.user.q_marks_by_url(form.url.data):
            flash('Mark with this url (%s) already\
                  exists.' % (form.url.data), category='error')
            return redirect(url_for('marks.allmarks'))
        form.populate_obj(m)
        m.updated = datetime.utcnow()
        db.session.add(m)
        db.session.commit()
        flash('Mark "%s" updated.' % (form.title.data), category='info')
        if form.referrer.data and is_safe_url(form.referrer.data):
            return redirect(form.referrer.data)
        return redirect(url_for('marks.allmarks'))
    """
    GET
    """
    form.referrer.data = request.referrer
    return render_template('mark/edit.html',
                           mark=m,
                           title='Edit mark - %s' % m.title,
                           form=form
                           )


@marks.route('/mark/delete/<int:id>')
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
        return redirect(url_for('marks.allmarks'))
    abort(403)


########
# AJAX #
########
@marks.route('/mark/inc')
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


###################
# Import / Export #
###################
@marks.route('/marks/export.json', methods=['GET'])
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


@marks.route('/marks/import', methods=['GET', 'POST'])
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
            return redirect(url_for('profile.view'))
        count = 0
        for c in data['marks']:
            m = Mark()
            m.insert_from_import(u.id, c)
            count += 1
            db.session.add(m)
            db.session.commit()
        flash('%s marks imported' % (count), category='info')
        return redirect(url_for('profile.view'))
    """
    GET
    """
    return render_template('profile/import.html',
                           form=form)


#########
# Other #
#########
@marks.route('/redirect/<int:id>')
@login_required
def mark_redirect(id):
    url = url_for('marks.mark_meta', id=id)
    return render_template('meta.html', url=url)


@marks.route('/meta/<int:id>')
@login_required
def mark_meta(id):
    b = g.user.bid(id)
    if b:
        return render_template('meta.html', url=b.url)
    abort(403)
