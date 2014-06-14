# flaskmarks/views/tags.py

from flask import Blueprint, render_template, g
from flask.ext.login import login_required

tags = Blueprint('tags', __name__)


@tags.route('/tags/cloud', methods=['GET'])
@login_required
def cloud():
    return render_template('tag/cloud.html',
                           title='Tag cloud',
                           header='',
                           tags=g.user.all_tags())


@tags.route('/tags/sort/clicks', methods=['GET'])
@tags.route('/tags/sort/clicks/<int:page>')
@login_required
def by_clicks(page=1):
    u = g.user
    return render_template('tag/index.html',
                           title='Tags - page %d' % page,
                           header='',
                           tags=u.tags_by_click(page))
