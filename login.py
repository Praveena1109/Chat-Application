from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c23761c3a31dc627ea1e638644ad7083'


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'pravinaacharya@gmail.com' and form.password.data == '123':
            flash('Logged in successfully!', 'success')
        else:
            flash('Login Unsuccessful. Please check email.id and password', 'danger')
    return render_template('login.html', title='Log In', form=form)


if __name__ == '__main__':
    app.run(debug=True)
