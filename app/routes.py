from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm, ChangeDataForm

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = ChangeDataForm()
    if request.method == 'POST' and form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            if form.change_username.data:
                current_user.username = form.username.data
                print(current_user.username)
            if form.change_email.data:
                current_user.email = form.email.data
            if form.change_password.data:
                hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                current_user.password = hashed_password
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Current password is incorrect', 'danger')
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.change_username.data = False
        form.change_email.data = False
        form.change_password.data = False
    return render_template('account.html', title='Account', form=form)