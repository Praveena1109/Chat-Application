from flask import render_template, url_for, flash, redirect, request
from main import app, db, bcrypt, socketio
from main.form import RegistrationForm, LoginForm, UpdateForm
from main.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send
import time
from PIL import Image
import secrets
import os

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
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
            next_page = request.args.get('next')
            flash('Successfully logged In', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Log In', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Successfully Logged Out', 'success')
    return redirect(url_for('home'))


@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat.html', title='Chat', name = current_user.firstName)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account has been updated", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', form = form, image_file=image_file)


@socketio.on('incoming-msg')
def on_message(data):
    msg = data["msg"]
    name = data["username"]

    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"username": name, "msg": msg, "time_stamp": time_stamp})
