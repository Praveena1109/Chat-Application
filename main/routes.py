from flask import render_template, url_for, flash, redirect, request, abort
from main import app, db, bcrypt, socketio, mail
from main.form import RegistrationForm, LoginForm, UpdateForm, PostForm, RequestResetForm, ResetPasswordForm
from main.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import emit
import time
from PIL import Image
import secrets
import os
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', title='Home', posts=posts)


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
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
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


def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not made this request then simply ignore this email and no changes will be done
'''
    mail.send(msg)


@app.route("/reset_request")
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('An email has been sent with instructions to reset password', 'info')
        return redirect(url_for('login'))
    return render_template('request_reset.html', title='reset password', form=form)


@app.route("/resent_password/<token>")
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_resent_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='reset password', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, information=form.information.data, sender=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Posted', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Post', form=form, legend='New post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.sender != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.information = form.information.data
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('home', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.information.data = post.information
    return render_template('create_post.html', title='Update post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.sender != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('home'))


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
        current_user.intro = form.intro.data
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
        form.intro.data = current_user.intro
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file=image_file)


@app.route("/info<int:post_id>", methods=['GET', 'POST'])
@login_required
def info(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('information.html', title='Information', post=post)

# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json)
