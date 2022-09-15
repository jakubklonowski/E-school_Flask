import logging
from flask import render_template, redirect, url_for, session
from flask_login import login_required, logout_user, login_user, current_user

from app import app, db
from app.forms import LoginForm, RegistrationForm, NewsForm, GradesForm
from app.models import News, Grade, User


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/news')
def news():
    newsy = News.query.all()
    return render_template('news.html', newsy=newsy)


@app.route('/grades', methods=['GET', 'POST'])
@login_required
def grades():
    user = User.query.filter_by(login=session['login']).first_or_404()

    if user.type == 'teacher':

        formG = GradesForm()
        if formG.validate_on_submit():
            g = Grade(subject=formG.subject.data, grade=formG.grade.data, student=formG.student.data)
            db.session.add(g)
            db.session.commit()
            app.logger.setLevel(logging.INFO)
            app.logger.info('Student whose id={} got grade {} from subject {}'.format(formG.student.data,
                                                                                     formG.grade.data,
                                                                                     formG.subject.data))
            return redirect(url_for('grades'))

        formN = NewsForm()
        if formN.validate_on_submit():
            n = News(title=formN.title.data, news=formN.news.data)
            db.session.add(n)
            db.session.commit()
            app.logger.setLevel(logging.INFO)
            app.logger.info('Added news {}'.format(formN.title.data))
            return redirect(url_for('news'))

        students = User.query.filter_by(type='student').all()
        return render_template('nauczyciel.html', students=students, formN=formN, formG=formG)

    elif not user.nauczyciel:
        studentGrades = Grade.query.filter_by(student=user.id).all()
        return render_template('uczen.html', grades=studentGrades)

    else:
        return render_template('401.html')


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/login_teacher', methods=['GET', 'POST'])
def login_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        teacher = User.query.filter_by().first()
        if teacher is None or not teacher.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(teacher)
        session['login'] = form.login.data
        return redirect('grades')
    return render_template('login_teacher.html', form=form)


@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        student = User.query.filter_by().first()
        if student is None or not student.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(student)
        session['login'] = form.login.data
        return redirect('grades')
    return render_template('login_student.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.nauczyciel:
            user = User(login=form.login.data, type='teacher')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            app.logger.setLevel(logging.INFO)
            app.logger.info('Registered user {} of type TEACHER'.format(form.login.data))
            return redirect(url_for('login'))
        elif not form.nauczyciel:
            user = User(login=form.login.data, type='student')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            app.logger.setLevel(logging.INFO)
            app.logger.info('Registered user {} of type STUDENT'.format(form.login.data))
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))
