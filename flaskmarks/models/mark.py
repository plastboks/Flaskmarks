from flaskmarks import db, config
from sqlalchemy import (
    and_,
    or_,
    desc,
)
from sqlalchemy.orm import relationship
from flaskmarks.models.meta import Meta

association_table = db.Table('mark_tags', db.metadata,
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
    tags = db.Column(db.Unicode(512))
    clicks = db.Column(db.Integer, default=0)
    last_clicked = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    metas = relationship('Meta', backref='mark', lazy='dynamic')
    ass_tags = relationship('Tag',
                            secondary=association_table,
                            backref='marks')

    @classmethod
    def by_tag(self, page, oID, per_page, tag):
        tag = "%"+tag+"%"
        return self.query.filter(and_(
                                 self.tags.like(tag),
                                 self.owner_id == oID))\
                         .order_by(desc(self.clicks))\
                         .paginate(page, per_page, False)

    @classmethod
    def by_string(self, page, oID, per_page, string, marktype=False):
        string = "%"+string+"%"
        base = self.query.filter(self.owner_id == oID)\
                         .filter(or_(self.title.like(string),
                                     self.tags.like(string),
                                     self.url.like(string)))
        if marktype:
            base = base.filter(self.type == marktype)
        base = base.order_by(desc(self.clicks))\
                   .paginate(page, per_page, False)
        return base

    def __repr__(self):
        return '<Mark %r>' % (self.title)
