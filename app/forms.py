from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')


class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password2 = PasswordField(
        'Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Login zajęty!')
