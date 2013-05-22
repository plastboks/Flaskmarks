from flaskmarks import db
import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), unique=True, nullable=False)
    email = db.Column(db.Unicode(255), unique=True, nullable=False)
    password = db.Column(db.Unicode(255), nullable=False)
    last_logged = db.Column(db.DateTime)
    #bookmarks = db.relationship('Bookmark', backref='owner_id', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)

    @classmethod
    def by_username(self, username):
        return self.query.filter(User.username == username).first()


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.Unicode(255), nullable=False)
    url = db.Column(db.Unicode(512), nullable=False)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<Bookmark %r>' % (self.title)
