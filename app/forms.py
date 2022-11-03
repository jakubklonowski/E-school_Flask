from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')


class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password2 = PasswordField('Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    teacher = BooleanField('Nauczyciel')
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Login zajęty!')


class GradesForm(FlaskForm):
    student = SelectField('Uczeń',
                          choices=[(s.id, '{}'.format(s.login)) for s in User.query.filter_by(type='student').all()],
                          validators=[DataRequired()])
    grade = SelectField('Ocena', choices=[(1, 'niedostateczny'),
                                          (2, 'dopuszczający'),
                                          (3, 'dostateczny'),
                                          (4, 'dobry'),
                                          (5, 'bardzo dobry'),
                                          (6, 'celujący')], validators=[DataRequired()])
    subject = SelectField('Przedmiot', choices=[('matematyka', 'matematyka'),
                                                ('j_polski', 'język polski'),
                                                ('j_angielski', 'język angielski')], validators=[DataRequired()])
    submit = SubmitField('Wstaw ocenę')


class NewsForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    news = TextAreaField('Treść', validators=[DataRequired()])
    submit = SubmitField('Opublikuj')
