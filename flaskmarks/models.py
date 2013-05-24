from flaskmarks import db
from sqlalchemy import and_
from cryptacular.bcrypt import BCRYPTPasswordManager
import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), unique=True, nullable=False)
    email = db.Column(db.Unicode(255), unique=True, nullable=False)
    password = db.Column(db.Unicode(255), nullable=False)
    last_logged = db.Column(db.DateTime)

    @classmethod
    def by_username(self, username):
        return self.query.filter(User.username == username).first()

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


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner_inc = db.Column(db.Integer)
    title = db.Column(db.Unicode(255), nullable=False)
    url = db.Column(db.Unicode(512), nullable=False)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    
    @classmethod
    def my_bookmarks(self, userid):
        return self.query.filter(self.owner_id == userid).all()

    @classmethod
    def by_id(self, oID, bID):
        return self.query.filter(and_(self.id == bID, self.owner_id == oID)).first()
    
    def __repr__(self):
        return '<Bookmark %r>' % (self.title)