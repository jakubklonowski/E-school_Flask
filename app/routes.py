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


# @app.route('/grades', methods=['GET', 'POST'])
# @login_required
# def grades():
#     user = User.query.filter_by(login=session['login']).first_or_404()  # uczen czy nauczyciel?
#
#     if user.nauczyciel:
#         formO = GradesForm()
#         if formO.validate_on_submit():
#             o = Ocena(przedmiot=formO.przedmiot.data, ocena=formO.ocena.data, uczen=formO.uczen.data)
#             db.session.add(o)
#             db.session.commit()
#             app.logger.setLevel(logging.INFO)
#             app.logger.info('Uczeń o id={} otrzymał ocenę {} z przedmiotu {}'.format(formO.uczen.data, formO.ocena.data,
#                                                                                      formO.przedmiot.data))
#             return redirect(url_for('oceny'))
#
#         formN = NewsForm()
#         if formN.validate_on_submit():
#             n = News(tytul=formN.tytul.data, tresc=formN.tresc.data)
#             db.session.add(n)
#             db.session.commit()
#             app.logger.setLevel(logging.INFO)
#             app.logger.info('Dodano news {}'.format(formN.tytul.data))
#             return redirect(url_for('news'))
#
#         uczniowie = User.query.filter_by(nauczyciel=False).all()
#         return render_template('nauczyciel.html', uczniowie=uczniowie, formN=formN, formO=formO)
#
#     elif not user.nauczyciel:
#         studentGrades = Ocena.query.filter_by(uczen=user.id).all()
#         return render_template('uczen.html', grades=studentGrades)
#     else:
#         return render_template('401.html')


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
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(login=form.login.data, nauczyciel=form.nauczyciel.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         app.logger.setLevel(logging.INFO)
#         app.logger.info(
#             'Zarejestrowano uzytkownika {} typu nauczyciel {}'.format(form.login.data, form.nauczyciel.data))
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))
