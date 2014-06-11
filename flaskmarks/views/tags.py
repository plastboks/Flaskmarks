# flaskmarks/views/tags.py

from flask import (
    Blueprint,
    render_template,
    g,
)
from flask.ext.login import login_required

tags = Blueprint('tags', __name__)


@tags.route('/tagcloud', methods=['GET'])
@login_required
def cloud():
    return render_template('tag/cloud.html',
                           title='Tag cloud',
                           header='',
                           tags=g.user.all_tags())


@tags.route('/tagsbyclicks', methods=['GET'])
@tags.route('/tagsbyclicks/<int:page>')
@login_required
def by_clicks(page=1):
    u = g.user
    return render_template('tag/index.html',
                           title='Tags - page %d' % page,
                           header='',
                           tags=u.tags_by_click(page))
