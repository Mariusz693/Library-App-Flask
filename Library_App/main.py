from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, \
    flash, make_response
from flask_login import login_required
from .models import UserType, db, Category, Author, Book, BooksUsers, User
from .forms import CategoryForm, AuthorForm, BookForm, BorrowForm
from .auth import access_decorate


main = Blueprint('main', __name__)


@main.context_processor
def context_data():

    return dict(
        admin=UserType.Admin.name,
        client=UserType.Client.name,
        today=date.today()
    )


@main.route('/')
def index():

    return render_template('index.html')


@main.route('/categories')
def categories():

    category_list=Category.query.order_by(Category.name).all()
    
    return render_template(
        template_name_or_list='categories.html',
        category_list=category_list
    )


@main.route('/category_details/<int:category_id>')
def category_details(category_id):

    category = Category.query.get_or_404(category_id)

    return render_template(
        template_name_or_list='category_details.html',
        category=category
    )


@main.route('/category_create', methods=['GET', 'POST'])
@login_required
@access_decorate
def category_create():

    form = CategoryForm()

    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.name.data).first()

        if category is None:
            category = Category(
                name=form.name.data,
            )
            db.session.add(category)
            db.session.commit()
            flash('Kategoria została utworzona', 'success')
        
        else:
            flash('Kategoria już istnieje w bazie', 'danger')
        
        return redirect(url_for('main.categories'))

    return render_template(
        template_name_or_list='category_create.html',
        form=form
    )


@main.route('/category_delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
@access_decorate
def category_delete(category_id):
    
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        
        db.session.delete(category)
        db.session.commit()
        flash('Kategoria została usunięta', 'success')
        
        return redirect(url_for('main.categories'))

    return render_template(
        template_name_or_list='delete.html',
        object_type='Kategoria',
        object=category,
        back_link=url_for('main.category_details', category_id=category.id)
    )


@main.route('/authors')
def authors():

    search = request.args.get('search')
    
    if search:
        authors_list = Author.query.filter(
            Author.name.ilike(f'{search}%')
        ).order_by(Author.name).all()
    
    else:
        authors_list = Author.query.order_by(Author.name).all()

    return render_template(
        template_name_or_list='authors.html',
        authors_list=authors_list
    )


@main.route('/author_details/<int:author_id>')
def author_details(author_id):
    
    author = Author.query.get_or_404(author_id)

    return render_template(
        template_name_or_list='author_details.html',
        author=author
    )


@main.route('/author_create', methods=['GET', 'POST'])
@login_required
@access_decorate
def author_create():

    form = AuthorForm()

    if form.validate_on_submit():
        author = Author.query.filter_by(name=form.name.data).first()

        if author is None:
            author = Author(
                name=form.name.data,
                date_of_birth=form.date_of_birth.data,
                date_of_death=form.date_of_death.data,
                biography=form.biography.data
            )
            db.session.add(author)
            db.session.commit()
            flash('Profil autora został utworzony', 'success')
        
        else:
            flash('Profil autora już istnieje w bazie', 'danger')

        return redirect(url_for('main.author_details', author_id=author.id))

    return render_template(
        template_name_or_list='author_form.html',
        form=form
    )


@main.route('/author_update/<int:author_id>', methods=['GET', 'POST'])
@login_required
@access_decorate
def author_update(author_id):
    
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)

    if form.validate_on_submit():
        author_check = Author.query.filter_by(name=form.name.data).first()

        if author_check and author_check != author:
            author = author_check
            flash('Profil autora już istnieje w bazie', 'danger')
        
        else:
            author.name = form.name.data
            author.date_of_birth = form.date_of_birth.data
            author.date_of_death = form.date_of_death.data
            author.biography = form.biography.data
            db.session.commit()
            flash('Profil autora został zakualizowany', 'success')

        return redirect(url_for('main.author_details', author_id=author.id))
        
    return render_template(
        template_name_or_list='author_form.html',
        form=form,
        author=author
    )


@main.route('/author_delete/<int:author_id>', methods=['GET', 'POST'])
@login_required
@access_decorate
def author_delete(author_id):
    
    author = Author.query.get_or_404(author_id)
    
    if request.method == 'POST':
        
        for book in author.books:
            if book.copies_borrowed > 0:
                flash('Książki na wypożyczeniu, wymagany ich zwrot', 'danger')
                
                return redirect(url_for('main.author_details', author_id=author.id))

        else:
            db.session.delete(author)
            db.session.commit()
            flash('Profil autora został usunięty', 'success')
        
            return redirect(url_for('main.authors'))

    flash('Wszystkie książki autora zostaną usunięte', 'danger')    

    return render_template(
        template_name_or_list='delete.html',
        object_type='Autor',
        object=author,
        back_link=url_for('main.author_details', author_id=author.id)
    )


@main.route('/books')
def books():

    search = request.args.get('search')

    if search:
        books_list = Book.query.filter(
            Book.title.ilike(f'{search}%')
        ).order_by(Book.title).all()
    
    else:
        books_list = Book.query.order_by(Book.title).all()


    return render_template(
        template_name_or_list='books.html',
        books_list=books_list
    )


@main.route('/book_details/<int:book_id>')
def book_details(book_id):
    
    book = Book.query.get_or_404(book_id)
    book_borrowed = BooksUsers.query.filter_by(
        book=book, date_of_returned=None
    ).order_by(
        BooksUsers.date_of_borrowed.desc()
    ).all()
    
    return render_template(
        template_name_or_list='book_details.html',
        book=book,
        book_borrowed=book_borrowed
    )


@main.route('/book_create', methods=['GET', 'POST'])
@login_required
@access_decorate
def book_create():
    
    form = BookForm()

    if form.validate_on_submit():
        book = Book.query.filter_by(isbn=form.isbn.data).first()

        if book is None:
            book = Book(
                isbn=form.isbn.data,
                title=form.title.data,
                description=form.description.data,
                copies=form.copies.data,
                author=form.author.data
            )
            book.categories=form.categories.data
            db.session.add(book)
            db.session.commit()
            flash('Profil książki został utworzony', 'success')

        else:
            flash('Numer ISBN już istnieje w bazie', 'danger')

        return redirect(url_for('main.book_details', book_id=book.id))

    return render_template(
        template_name_or_list='book_form.html',
        form=form,
        form_author=AuthorForm(),
        form_category=CategoryForm()
    )


@main.route('/book_create_author', methods=['POST'])
@login_required
@access_decorate
def book_create_author():
    
    data = request.get_json(force=True)
    form = AuthorForm(data=data)
        
    if form.validate():
        author = Author.query.filter_by(name=form.name.data).first()

        if author is None:
            author = Author(
                name=form.name.data,
                date_of_birth=form.date_of_birth.data,
                date_of_death=form.date_of_death.data
            )
            db.session.add(author)
            db.session.commit()
            answer = {
                'status': 'create',
                'author': {
                    'name': author.name,
                    'id': str(author.id)
                }
            }
        
        else:
            answer = {
                'status': 'exist',
                'id': str(author.id)
            }

    else:
        answer = {
            'status': 'error',
            'errors': {
                'name': form.name.errors,
                'date_of_birth': form.date_of_birth.errors,
                'date_of_death': form.date_of_death.errors
            }
        }
        
    return make_response(answer, 200)


@main.route('/book_create_category', methods=['POST'])
@login_required
@access_decorate
def book_create_category():
    
    data = request.get_json(force=True)
    form = CategoryForm(data=data)
    
    if form.validate():
        category = Category.query.filter_by(name=form.name.data).first()

        if category is None:
            category = Category(
                name=form.name.data,
            )
            db.session.add(category)
            db.session.commit()
            answer = {
                'status': 'create',
                'category': {
                    'name': category.name,
                    'id': str(category.id)
                }
            }
        
        else:
            answer = {
                'status': 'exist',
                'id': str(category.id)
            }
    
    else:
        answer = {
            'status': 'error',
            'errors': {
                'name': form.name.errors
            }
        }
        
    return make_response(answer, 200)


@main.route('/book_update/<int:book_id>', methods=['GET', 'POST'])
@login_required
@access_decorate
def book_update(book_id):
    
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book_check = Book.query.filter_by(isbn=form.isbn.data).first()

        if book_check and book_check != book:
            book = book_check
            flash('Numer ISBN już istnieje w bazie', 'danger')
        
        elif form.copies.data < book.copies_borrowed:
            flash('Ilość woluminów na wypożyczeniu większa niż podana', 'danger')

        else:
            book.isbn=form.isbn.data, 
            book.title=form.title.data,
            book.description=form.description.data,
            book.copies=form.copies.data,
            book.author=form.author.data
            book.categories=form.categories.data
            db.session.commit()
            flash('Profil książki został zakualizowany', 'success')

        return redirect(url_for('main.book_details', book_id=book.id))

    return render_template(
        template_name_or_list='book_form.html',
        form=form,
        book=book,
        form_author=AuthorForm(),
        form_category=CategoryForm()
    )


@main.route('/book_delete/<int:book_id>', methods=['GET', 'POST'])
@login_required
@access_decorate
def book_delete(book_id):
    
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        
        if book.copies_borrowed > 0:
            flash('Woluminy na wypożyczeniu, wymagany ich zwrot', 'danger')
                
            return redirect(url_for('main.book_details', book_id=book.id))

        else:
            db.session.delete(book)
            db.session.commit()
            flash('Profil książki został usunięty', 'success')
        
            return redirect(url_for('main.books'))

    flash('Historia wypożyczeń książki zostanie usunięta', 'danger')    

    return render_template(
        template_name_or_list='delete.html',
        object_type='Książka',
        object=book,
        back_link=url_for('main.book_details', book_id=book.id)
    )


@main.route('/book_borrows/<int:book_id>')
@login_required
@access_decorate
def book_borrows(book_id):

    search = request.args.get('search')
    book = Book.query.get_or_404(book_id)
    book_borrowed = BooksUsers.query.filter(
        BooksUsers.book==book, BooksUsers.date_of_returned!=None
    ).order_by(
        BooksUsers.date_of_returned.desc(),
        BooksUsers.date_of_borrowed.desc()
    ).all()
    
    if search:
        users = User.query.filter(
            User.last_name.ilike(f'{search}%')
        ).all()
        book_borrowed = [item for item in book_borrowed if item.user in users]

    return render_template(
        template_name_or_list='book_borrows.html',
        book=book,
        book_borrowed=book_borrowed
    )


@main.route('/book_borrow/<int:book_id>', methods=['GET', 'POST'])
@login_required
@access_decorate
def book_borrow(book_id):
    
    book = Book.query.get_or_404(book_id)
    form = BorrowForm()
    
    if form.validate_on_submit():
        user = form.user.data
        book_user = BooksUsers.query.filter(
            BooksUsers.book==book,
            BooksUsers.user==user,
            BooksUsers.date_of_returned==None
        ).first()
        
        if book.copies_borrowed >= book.copies:
            flash('Wszystie woluminy książki już wypożyczone', 'danger')

        elif book_user:
            flash('Książka już wypożyczona przez użytkownika', 'danger')

        else:
            book_user = BooksUsers(
                book=book,
                user=user,
                date_of_borrowed=date.today()
            )
            db.session.add(book_user)
            book.copies_borrowed += 1
            db.session.commit()
            flash('Książka wypożyczona przez użytkownika', 'success')

        return redirect(url_for('main.book_details', book_id=book.id))

    return render_template(
        template_name_or_list='book_borrow.html',
        book=book,
        form=form
    )


@main.route('/book_return/<int:book_user_id>', methods=['GET', 'POST'])
@login_required
@access_decorate
def book_return(book_user_id):
    
    book_user = BooksUsers.query.get_or_404(book_user_id)
    next_page = request.args.get('next')
    back_link = next_page or url_for('main.book_details', book_id=book_user.book.id)

    if request.method == 'POST':
        book_user.date_of_returned = date.today()
        book_user.book.copies_borrowed -= 1
        db.session.commit()
        flash('Książka została zwrócona przez użytkownika', 'success')

        return redirect(back_link)

    return render_template(
        template_name_or_list='book_return.html',
        book_user=book_user,
        back_link=back_link
    )