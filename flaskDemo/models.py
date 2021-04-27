from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"Users('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Test(db.Model):
    __table__ = db.Model.metadata.tables['test']
    
class Testing_Site(db.Model):
    __table__ = db.Model.metadata.tables['testing_site']
class Users(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['users']
class Vaccination(db.Model):
    __table__ = db.Model.metadata.tables['vaccination']
class Vaccination_Site(db.Model):
    __table__ = db.Model.metadata.tables['vaccination_site']
class Vaccine(db.Model):
    __table__ = db.Model.metadata.tables['vaccine']
