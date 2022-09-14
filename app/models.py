from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    type = db.Column(db.String(10))  # this is the discriminator column

    __mapper_args__ = {
        'polymorphic_on': type,
    }

    def __repr__(self):
        return '<{} {}>'.format(self.type, self.login)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    grades = db.relationship('Grade', backref='student_', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64))
    grade = db.Column(db.String(64))
    student = db.Column(db.Integer, db.ForeignKey('student.id'))


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    news = db.Column(db.String(800))

    def __repr__(self):
        return '<News {} to {}>'.format(self.title, self.news)
