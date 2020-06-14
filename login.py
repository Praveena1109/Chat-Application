from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c23761c3a31dc627ea1e638644ad7083'


@app.route("/", methods=['GET', '_POST_'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'_Account created for {form.email.data}!_', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Log In', form=form)


if __name__ == '__main__':
    app.run(debug=True)
