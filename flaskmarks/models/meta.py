from flaskmarks import db, config
from sqlalchemy import (
    and_,
    or_,
    desc,
)


class Meta(db.Model):
    __tablename__ = 'meta'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Unicode(255), nullable=False)
    value = db.Column(db.Unicode(255), nullable=False)

    def __repr__(self):
        return '<Meta %r>' % (self.title)
