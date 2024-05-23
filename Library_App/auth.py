from datetime import datetime
from flask import Blueprint, flash, redirect, url_for, request, \
    render_template
from flask_login import login_user, login_required, logout_user, \
     current_user
from .forms import UserLoginForm, UserCreateForm, UserUpdateForm, \
    UserPasswordForm
from .models import User, db, UserType, BooksUsers
from . import login_manager


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):

    if user_id is not None:

        return User.query.get(user_id)
    
    return None
 

@login_manager.unauthorized_handler
def unauthorized():

    flash('Zaloguj się aby wejść na tą stronę', 'danger')

    return redirect(url_for('auth.user_login') + f'?next={request.path}')


@auth.route('/user_login', methods=['GET', 'POST'])
def user_login():

    if current_user.is_authenticated:

        return redirect(url_for('main.index'))
    
    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(password=form.password.data):
            login_user(user=user)
            user.date_of_last_login = datetime.now()
            db.session.commit()
            next_page = request.args.get('next')

            return redirect(next_page or url_for('main.index'))
        
        elif user:
            flash('Hasło nieprawidłowe.', 'danger')

        else:
            flash('Adres Email nieprawidłowy, brak użykownika', 'danger')
    
    return render_template(
        template_name_or_list='user_login.html',
        form=form
    )


@auth.route('/user_create', methods=['GET', 'POST'])
def user_create():

    form = UserCreateForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                date_of_created=datetime.now()
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Profil został utworzony', 'success')

            return redirect(url_for('auth.user_login'))
        
        flash('Adres Email już istnieje w bazie.', 'danger')
    
    return render_template(
        template_name_or_list='user_create.html',
        form=form
    )


@auth.route('/user_logout')
@login_required
def user_logout():
    
    logout_user()

    return redirect(url_for('main.index'))


@auth.route('/user_profile')
@login_required
def user_profile():

    returned = request.args.get('returned')
    
    if returned == 'True':
        book_borrowed = BooksUsers.query.filter(
            BooksUsers.user==current_user, BooksUsers.date_of_returned!=None
        ).order_by(
            BooksUsers.date_of_returned.desc(),
            BooksUsers.date_of_borrowed.desc()
        ).all()

    else:
        book_borrowed = BooksUsers.query.filter(
            BooksUsers.user==current_user, BooksUsers.date_of_returned==None
        ).order_by(
            BooksUsers.date_of_borrowed.desc()
        ).all()

    return render_template(
        template_name_or_list='user_profile.html',
        book_borrowed=book_borrowed
    )


@auth.route('/user_update', methods=['GET', 'POST'])
@login_required
def user_update():
    
    form = UserUpdateForm(obj=current_user)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user == current_user or user == None:
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.phone_number = form.phone_number.data
            db.session.commit()
            flash('Profil został zakualizowany', 'success')

            return redirect(url_for('auth.user_profile'))
        
        flash('Adres Email należy do innego użytkownika.', 'danger')
    
    return render_template(
        template_name_or_list='user_update.html',
        form=form
    )


@auth.route('/user_password', methods=['GET', 'POST'])
@login_required
def user_password():
    
    form = UserPasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(password=form.password.data):
            current_user.set_password(form.password_new.data)
            db.session.commit()
            logout_user()
            flash('Hasło zaktualizowane', 'success')

            return redirect(url_for('auth.user_login'))

        flash('Hasło nieprawidłowe.', 'danger')
    
    return render_template(
        template_name_or_list='user_password.html',
        form=form
    )


@auth.route('/user_delete', methods=['GET', 'POST'])
@login_required
def user_delete():
    
    if request.method == 'POST':
        admin_count = User.query.filter_by(status=UserType.Admin.name).count()
        
        if current_user.status == UserType.Admin and admin_count < 2:
            flash('Jedyny administrator, nie można usunąć profilu', 'danger')

            return redirect(url_for('auth.user_profile'))

        else:
            for borrowed_books in current_user.books:
                if borrowed_books.date_of_returned is None:
                    flash('Książki na wypożyczeniu, nie można usunąć profilu', 'danger')
                    
                    return redirect(url_for('auth.user_profile'))
            
            else:
                db.session.delete(current_user)
                db.session.commit()

                return redirect(url_for('main.index'))
            
    return render_template(
        template_name_or_list='delete.html',
        object_type='Użytkownik',
        object=current_user,
        back_link=url_for('auth.user_profile')
    )