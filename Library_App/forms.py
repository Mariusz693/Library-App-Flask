from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, Regexp, \
    EqualTo
from .validators import PasswordValidator


class UserLoginForm(FlaskForm):

    email = StringField(
        label='Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Email(message='Adres email nie poprawny!')
        ]
    )
    password = PasswordField(
        label='Hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!')
        ]
    )
    submit = SubmitField('Zaloguj')


class UserCreateForm(FlaskForm):

    first_name = StringField(
        label='Imię: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Length(max=256)
        ]
    )
    last_name = StringField(
        label='Nazwisko: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Length(max=256)
        ]
    )
    email = StringField(
        label='Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Email(message='Adres email nie poprawny!'),
            Length(max=256)
        ]
    )
    phone_number = StringField(
        label='Numer telefonu:',
        validators=[
            Optional(),
            Length(min=9, max=9),
            Regexp('^[0-9]*$', message='Numer telefonu może składać się tylko z cyfr!')
        ]
    )
    password = PasswordField(
        label='Hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            PasswordValidator()
        ]
    )
    password_repeat = PasswordField(
        label='Powtórz hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            EqualTo('password', message='Hasła muszą być identyczne!')
        ]
    )
    submit = SubmitField('Zapisz')


class UserUpdateForm(FlaskForm):

    first_name = StringField(
        label='Imię: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Length(max=256)
        ]
    )
    last_name = StringField(
        label='Nazwisko: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Length(max=256)
        ]
    )
    email = StringField(
        label='Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Email(message='Adres email nie poprawny!'),
            Length(max=256)
        ]
    )
    phone_number = StringField(
        label='Numer telefonu:',
        validators=[
            Optional(),
            Length(min=9, max=9),
            Regexp('^[0-9]*$', message='Numer telefonu może składać się tylko z cyfr!')
        ]
    )
    submit = SubmitField('Zapisz')


class UserPasswordForm(FlaskForm):

    password = PasswordField(
        label='Hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!')
        ]
    )
    password_new = PasswordField(
        label='Nowe hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            PasswordValidator()
        ]
    )
    password_repeat = PasswordField(
        label='Powtórz hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            EqualTo('password_new', message='Hasła muszą być identyczne!')
        ]
    )
    submit = SubmitField('Zapisz')