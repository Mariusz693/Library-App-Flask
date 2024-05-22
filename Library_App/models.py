import enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class UserType(enum.Enum):
    Admin = 'Administrator'
    Client = 'Klient'


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), unique=False, nullable=False)
    last_name = db.Column(db.String(256), unique=False, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    phone_number = db.Column(db.String(9), unique=False, nullable=False)
    status = db.Column(db.Enum(UserType), default=u'Client', server_default=u'Client', nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    date_of_created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    date_of_last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    books = db.relationship('BooksUsers', back_populates='user', cascade='all, delete')

    def set_password(self, password):
        
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        
        return '<id {} - user, {} - status>'.format(self.id, self.status)
    
    def __str__(self):
        
        return '{} {}'.format(self.first_name, self.last_name)


class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(256), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    copies = db.Column(db.Integer, unique=False, nullable=False)
    copies_borrowed = db.Column(db.Integer, default=u'0', server_default=u'0', unique=False, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), nullable=False, unique=False)
    author = db.relationship('Author', back_populates='books')
    categories =  db.relationship('Category', secondary='books_categories', back_populates='books')
    users = db.relationship('BooksUsers', back_populates='book', cascade='all, delete')

    def __repr__(self):

        return '<id {} - book>'.format(self.id)
    
    def __str__(self):

        return self.title


class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, unique=False, nullable=False)
    date_of_death = db.Column(db.Date, unique=False, nullable=True)
    biography = db.Column(db.Text, unique=False, nullable=True)
    books = db.relationship('Book', back_populates='author', cascade='all, delete')

    def __repr__(self):

        return '<id {} - author>'.format(self.id)
    
    def __str__(self):

        return self.name


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    books = db.relationship('Book', secondary='books_categories', back_populates='categories')

    def __repr__(self):

        return '<id {} - category>'.format(self.id)
    
    def __str__(self):

        return self.name


class BooksUsers(db.Model):

    __tablename__ = 'books_users'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey('books.id', ondelete='CASCADE'), unique=False, nullable=False)
    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), unique=False, nullable=False)
    book = db.relationship('Book', back_populates='users')
    user = db.relationship('User', back_populates='books')
    date_of_borrowed = db.Column(db.Date, unique=False, nullable=False)
    date_of_returned = db.Column(db.Date, unique=False, nullable=True)

    def __repr__(self):
        
        return '<id {} - book_user, {} - book, {} - user>'.format(self.id, self.book_id, self.user_id)


books_categories = db.Table(

    'books_categories',

    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
    db.Column('category_id', db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
)