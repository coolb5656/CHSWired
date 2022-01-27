from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from flask_login import login_required, current_user
from .models import item, student, reservation, log

main = Blueprint('main', __name__)

@main.route("/profile")
@login_required
def profile():
    if(current_user.pos == "Producer"):
        return render_template("admin/profile.html", name=current_user.name)
    return redirect(url_for('main.view_student', id=current_user.id))

@main.route("/items") # view all items
def view_items():
    items = item.query.all()
    return render_template("views/items.html", items=items)

@main.route("/item/<id>") # view item
def view_item(id):
    i = item.query.filter_by(id=id).first_or_404()
    return render_template("views/item.html", item=i)

@main.route("/students") # view all students
def view_students():
    students = student.query.all()
    return render_template("views/students.html", students=students)

@main.route("/student/<id>") # view student
def view_student(id):
    s = student.query.filter_by(id=id).first_or_404()
    return render_template("views/student.html", student=s)

@main.route("/reservations") # view all reservations
def view_reservations():
    reservations = reservation.query.all()
    return render_template("views/reservations.html", reservations=reservations)

@main.route("/reservation/<id>") # view reservation
def view_reservation(id):
    r = reservation.query.filter_by(id=id).first_or_404()
    return render_template("views/reservation.html", reservation=r)

@main.route("/log") # view all reservations
def view_log():
    logs = log.query.all()
    return render_template("views/log.html", logs=logs)