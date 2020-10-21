from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from qaf import db, bcrypt
from qaf.models import User
from qaf.forms.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from qaf.utils import save_picture, send_reset_token


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, expert=True, admin=False)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. Now you can log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register',form=form)


@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            flash('You have been logged in', 'info')
            #return redirect(next_page) if next_page else redirect(url_for('main.home'))
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful','error')
    return render_template('login.html', title='Login',form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@auth.route("/users")
def users():
    users = User.query.all()
    return render_template('users.html', title='users', users=users)


@auth.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_token(user)
        flash('An Email has been sent with instruction to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth.route("/reset_password/<token>", methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid Token or expired token','warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated. Now you can log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', title='Reset Password', form=form)


@auth.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('You account has been updated', 'info')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)



@auth.route('/debug_add', methods=['GET','POST'])
def ads():
    password = '123456'
    email = 'metalika123@gmail.com'
    username = 'jacek123'
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Your account has been created. Now you can log in', 'success')
    return redirect(url_for('auth.login'))


