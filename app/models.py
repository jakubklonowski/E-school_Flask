from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    nauczyciel = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}, typu nauczyciel: {}>'.format(self.login, self.nauczyciel)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class News(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tytul = db.Column(db.String(64))
    tresc = db.Column(db.String(800))

    def __repr__(self):
        return '<News {} to {}>'.format(self.tytul, self.tresc)
