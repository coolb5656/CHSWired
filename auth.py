from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import student
from . import db
from flask_login import login_user, login_required, logout_user


def new_student(name, email, password):
    existing_student = student.query.filter_by(email=email).first()

    if existing_student:
        flash('Email address already exists')
        return 0

    new = student(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new)
    db.session.commit()
    return 1

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("pwd")

        s = student.query.filter_by(email=email).first()

        if not s or not check_password_hash(s.pwd, password):
            flash("Wrong Email or Password!")
            return redirect(url_for("auth.login"))
        
        login_user(s)
        return redirect(url_for('main.profile'))

    return render_template('auth/login.html', error=error)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # code to validate and add user to database goes here
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('pwd')

        user = student.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists!')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = student(email=email, name=name, pos="Student",pwd=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))