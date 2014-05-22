from flaskmarks import db, config
from sqlalchemy import (
    and_,
    or_,
    desc,
)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Tag %r>' % (self.title)
