from flask import render_template, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user
from application import db, app
from application.all_users.users import User
from application.ticket_system.auth.forms import LoginForm


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


class RegistrationForm:
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/analysts')
@login_required
def analysts():
    return redirect(url_for('analysts.index'))


@app.route('/users')
@login_required
def users():
    return redirect(url_for('urls.py.index'))


def user_bp():
    return None