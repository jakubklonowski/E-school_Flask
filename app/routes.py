import logging
from flask import render_template, redirect, url_for, session, request
from flask_login import login_required, logout_user, login_user, current_user

from app import app, db
from app.forms import LoginForm, RegistrationForm, NewsForm, GradesForm
from app.models import News, Grade, User


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'GET':
        try:
            user = User.query.filter_by(login=session['login']).first()
            if user.type == 'teacher':
                newsy = News.query.all()
                return render_template('news_teacher.html', newsy=newsy)
        except:
            newsy = News.query.all()
            return render_template('news.html', newsy=newsy)
    elif request.method == 'POST':
        try:
            if request.form['method_name'] == 'DELETE':
                data = request.form
                post = data['del_name']
                n = News.query.filter_by(id=post).first()
                db.session.delete(n)
                db.session.commit()
                app.logger.setLevel(logging.INFO)
                app.logger.info('Removed news with ID={}'.format(post))
                return redirect(url_for('news'))
            else:
                data = request.form
                id = data['edit_name']
                return redirect('news_edit/' + id)
        except:
            return redirect(url_for('news'))


@app.route('/news_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def news_edit(id):
    formN = NewsForm()
    n = News.query.filter_by(id=id).first_or_404()

    if request.method == 'GET':
        formN.title.data = n.title
        formN.news.data = n.news
        return render_template('news_edit.html', formN=formN, news=news)

    elif request.method == 'POST':
        if formN.validate_on_submit():
            n.title = formN.title.data
            n.news = formN.news.data
            db.session.commit()
            app.logger.setLevel(logging.INFO)
            app.logger.info('News with id={} was edited to {}'.format(id, formN.title.data))
            return redirect(url_for('news'))


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
        return render_template('teacher.html', students=students, formN=formN, formG=formG)

    elif user.type == 'student':
        studentGrades = Grade.query.filter_by(student=user.id).all()
        return render_template('student.html', grades=studentGrades)

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
        teacher = User.query.filter_by(login=form.login.data).first()
        if teacher is None or not teacher.check_password(form.password.data):
            return redirect(url_for('login_teacher'))
        login_user(teacher)
        session['login'] = form.login.data
        app.logger.setLevel(logging.INFO)
        app.logger.info('Logged in user {} of type TEACHER'.format(form.login.data))
        return redirect('grades')
    return render_template('login_teacher.html', form=form)


@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        student = User.query.filter_by(login=form.login.data).first()
        if student is None or not student.check_password(form.password.data):
            return redirect(url_for('login_student'))
        login_user(student)
        session['login'] = form.login.data
        app.logger.setLevel(logging.INFO)
        app.logger.info('Logged in user {} of type STUDENT'.format(form.login.data))
        return redirect('grades')
    return render_template('login_student.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.teacher.data:
            user = User(login=form.login.data, type='teacher')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            app.logger.setLevel(logging.INFO)
            app.logger.info('Registered user {} of type TEACHER'.format(form.login.data))
            return redirect(url_for('login'))
        elif not form.teacher.data:
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
