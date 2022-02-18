from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.models import db,student
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("pwd")

        pos_allowed_login = ["Producer", "Teacher"]

        s = student.query.filter_by(email=email).first()


        if not s or not check_password_hash(s.pwd, password):
            flash("Wrong Email or Password!", "Error")
            return redirect(url_for("auth.login"))
        elif s.pos not in pos_allowed_login:
            flash("You must be a Producer to access this page!", "Error")
            return redirect(url_for("index"))

        login_user(s)
        return redirect(url_for('admin.profile'))

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
            flash('Email address already exists!', "Error")
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = student(email=email, name=name, pos="Teacher",pwd=generate_password_hash(password, method='sha256'))

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