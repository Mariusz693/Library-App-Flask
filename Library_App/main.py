from flask import Blueprint, render_template, request, redirect, url_for, \
    flash
from flask_login import login_required
from .models import UserType, db, Category
from .forms import CategoryForm
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