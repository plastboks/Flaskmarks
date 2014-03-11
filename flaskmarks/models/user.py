from flaskmarks import db, config
from sqlalchemy import (
    or_,
    desc,
    asc,
    func,
)
from cryptacular.bcrypt import BCRYPTPasswordManager
from flaskmarks.models.mark import Mark


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), unique=True, nullable=False)
    email = db.Column(db.Unicode(255), unique=True, nullable=False)
    password = db.Column(db.Unicode(255), nullable=False)
    last_logged = db.Column(db.DateTime)
    per_page = db.Column(db.SmallInteger, default=10)
    suggestion = db.Column(db.SmallInteger, default=1)
    recently = db.Column(db.SmallInteger, default=2)
    sort_type = db.Column(db.Unicode(255), default=u'clicks')

    marks = db.relationship('Mark', backref='owner', lazy='dynamic')

    @classmethod
    def by_uname_or_email(self, uname):
        return self.query.filter(or_(User.username == uname,
                                     User.email == uname)).first()

    def my(self):
        return Mark.query.filter(Mark.owner_id == self.id)

    def suggestions(self, page):
        base = self.my().filter(Mark.clicks == 0)\
                        .order_by(func.random())
        return base.paginate(page, self.per_page, False)

    def recent(self, page, type):
        if type == 'added':
            base = self.my().order_by(asc(Mark.created))
            return base.paginate(page, self.per_page, False)
        if type == 'clicked':
            base = self.my().filter(Mark.clicks > 0)\
                            .order_by(asc(Mark.last_clicked))
            return base.paginate(page, self.per_page, False)
        return False;

    def marks(self, page):
        base = self.my()
        if self.sort_type == u'clicks':
            base = base.order_by(desc(Mark.clicks))\
                       .order_by(desc(Mark.created))
        if self.sort_type == u'dateasc':
            base = base.order_by(asc(Mark.created))
        if self.sort_type == u'datedesc':
            base = base.order_by(desc(Mark.created))
        return base.paginate(page, self.per_page, False)

    def mid(self, id):
        return self.my().filter(Mark.id == id)\
                        .first()

    def murl(self, string):
        return self.my().filter(Mark.url == string)\
                        .first()

    def mark_count(self):
        return self.my().count()

    def bookmark_count(self):
        return self.my().filter(Mark.type == 'bookmark').count()

    def feed_count(self):
        return self.my().filter(Mark.type == 'feed').count()

    def mark_last_created(self):
        return self.my().order_by(desc(Mark.created)).first()

    def tag(self, tag, page):
        return Mark.by_tag(page, self.id, self.per_page, tag)

    def string(self, page, string, marktype):
        return Mark.by_string(page, self.id, self.per_page, string, marktype)

    def authenticate_user(self, password):
        manager = BCRYPTPasswordManager()
        return manager.check(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
