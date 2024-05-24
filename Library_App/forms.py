from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, \
    TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Optional, Length, Regexp, \
    EqualTo, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField, QueryCheckboxField
from .validators import PasswordValidator, DateRangeValidator, EqualDateToValidator
from .models import Author, Category


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


class CategoryForm(FlaskForm):

    name = StringField(
        label='Kategoria: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Length(max=256)
        ]
    )
    submit = SubmitField('Zapisz')


class AuthorForm(FlaskForm):

    name = StringField(
        label='Imię i Nazwisko (Pseudonim): *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Length(max=256)
        ]
    )
    date_of_birth = DateField(
        label='Data urodzenia: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            DateRangeValidator()
        ]
    )
    date_of_death = DateField(
        label='Data śmierci:',
        validators=[
            Optional(),
            DateRangeValidator(),
            EqualDateToValidator(field_name='date_of_birth')
        ]
    )
    biography = TextAreaField(
        label='Biografia:',
        render_kw={'rows':'8'},
        validators=[Optional()]
    )
    submit = SubmitField('Zapisz')


class BookForm(FlaskForm):

    def query_choices_authors():

        return Author.query.order_by(Author.name).all()
        
    def query_choices_categories():

        return Category.query.order_by(Category.name).all()
    
    title = StringField(
        label='Tytuł: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Length(max=256)
        ]
    )
    isbn = StringField(
        label='ISBN: *',
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            Length(min=13, max=13),
            Regexp('^[0-9]*$', message='Numer ISBN może składać się tylko z cyfr!')
        ]
    )
    description = TextAreaField(
        label='Opis:',
        render_kw={'rows':'8'},
        validators=[Optional()]
    )
    copies = IntegerField(
        label='Woluminy: *',
        default=1,
        validators=[
            DataRequired(message='Pole obowiązkowe!'),
            NumberRange(min=1, message='Wymagany minimalnie jeden wolumin!')
        ]
    )
    author = QuerySelectField(
        label='Autor: *',
        query_factory=query_choices_authors,
        allow_blank=True,
        blank_text='Wybierz',
        validators=[
            DataRequired(message='Pole obowiązkowe!')
        ]
    )
    categories = QueryCheckboxField(
        label='Kategorie:',
        query_factory=query_choices_categories,
        validators=[Optional()]
    )
    submit = SubmitField('Zapisz')