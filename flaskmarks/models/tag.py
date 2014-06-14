# flaskmarks/models/tag.py

from sqlalchemy import and_, or_, desc
from ..core.setup import db, config


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)

    def __init__(self, title):
        self.title = title

    @classmethod
    def check(self, title):
        return self.query.filter(Tag.title == title).first()

    def __repr__(self):
        return '<Tag %r>' % (self.title)
