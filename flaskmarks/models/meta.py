# flaskmarks/models/meta.py

from sqlalchemy import and_, or_, desc
from ..core.setup import db, config


class MarksMeta(db.Model):
    __tablename__ = 'marksmeta'
    id = db.Column(db.Integer, primary_key=True)
    mark_id = db.Column(db.Integer, db.ForeignKey('marks.id'))
    name = db.Column(db.Unicode(255), nullable=False)
    value = db.Column(db.Unicode(255), nullable=False)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<MarksMeta %r>' % (self.name)


class UserMeta(db.Model):
    __tablename__ = 'usermeta'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Unicode(255), nullable=False)
    value = db.Column(db.Unicode(255), nullable=False)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<UserMeta %r>' % (self.name)
