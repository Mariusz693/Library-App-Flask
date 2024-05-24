from flask import Blueprint, render_template, request, redirect, url_for, \
    flash
from flask_login import login_required
from .models import UserType, db, Category, Author
from .forms import CategoryForm, AuthorForm
from .auth import access_decorate


main = Blueprint('main', __name__)


@main.context_processor
def context_data():

    return dict(
        admin=UserType.Admin.name,
        client=UserType.Client.name,
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
    authors_list = Author.query.order_by(Author.name).all()

    if search:
        authors_list = Author.query.filter(
            Author.name.ilike(f'{search}%')
        ).order_by(Author.name).all()

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