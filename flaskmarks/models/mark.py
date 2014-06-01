from flaskmarks import db, config
from sqlalchemy import (
    and_,
    or_,
    desc,
)
from sqlalchemy.orm import relationship
from flaskmarks.models.meta import Meta

ass_tbl = db.Table('marks_tags', db.metadata,
                   db.Column('left_id', db.Integer, db.ForeignKey('marks.id')),
                   db.Column('right_id', db.Integer, db.ForeignKey('tags.id'))
                   )


class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Unicode(255), nullable=False)
    title = db.Column(db.Unicode(255), nullable=False)
    url = db.Column(db.Unicode(512), nullable=False)
    clicks = db.Column(db.Integer, default=0)
    last_clicked = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    metas = relationship('Meta', backref='mark', lazy='dynamic')
    tags = relationship('Tag',
                        secondary=ass_tbl,
                        backref='marks')

    def __repr__(self):
        return '<Mark %r>' % (self.title)
