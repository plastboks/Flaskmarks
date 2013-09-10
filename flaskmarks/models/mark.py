from flaskmarks import db, config
from sqlalchemy import (
    and_,
    or_,
    desc,
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

    @classmethod
    def by_tag(self, page, oID, per_page, tag):
        tag = "%"+tag+"%"
        return self.query.filter(and_(
                                 self.tags.like(tag),
                                 self.owner_id == oID))\
                         .order_by(desc(self.clicks))\
                         .paginate(page, per_page, False)

    @classmethod
    def by_string(self, page, oID, per_page, string):
        string = "%"+string+"%"
        return self.query.filter(self.owner_id == oID)\
                         .filter(or_(self.title.like(string),
                                     self.tags.like(string),
                                     self.url.like(string)))\
                         .order_by(desc(self.clicks))\
                         .paginate(page, per_page, False)

    def __repr__(self):
        return '<Mark %r>' % (self.title)
