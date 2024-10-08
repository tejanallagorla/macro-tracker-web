from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# create auth blueprint
auth = Blueprint('auth', __name__)

# define login route inside auth
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # read login form input
        email = request.form.get('email')
        password = request.form.get('password')

        # validate login request
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('An account with that email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# define logout route inside auth
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

# define sign up route inside auth
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # read sign up form input
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # validate sign up request
        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account with that email already exists.', category='error')
        elif len(email) < 3:
            flash('Email must be at least 3 characters long.', category='error')
        elif len(email) > 75:
            flash('Email must be at most 75 characters long.', category='error')
        elif len(first_name) < 1:
            flash('First name must be at least 1 character long.', category='error')
        elif len(first_name) > 25:
            flash('First name must be at most 25 characters long.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        elif len(password1) > 20:
            flash('Password must be at most 20 characters long.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
