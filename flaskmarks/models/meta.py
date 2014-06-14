# flaskmarks/models/meta.py

from sqlalchemy import and_, or_, desc
from ..core.setup import db, config


class Meta(db.Model):
    __tablename__ = 'meta'
    id = db.Column(db.Integer, primary_key=True)
    mark_id = db.Column(db.Integer, db.ForeignKey('marks.id'))
    name = db.Column(db.Unicode(255), nullable=False)
    value = db.Column(db.Unicode(255), nullable=False)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<Meta %r>' % (self.title)
