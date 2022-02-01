from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.models import db,item, student, reservation, log

main = Blueprint('main', __name__)


######## ITEMS #############
@main.route("/items") # view all items
def view_items():
    items = item.query.all()
    return render_template("views/items.html", items=items)

@main.route("/item/<id>") # view item
def view_item(id):
    i = item.query.filter_by(id=id).first_or_404()
    return render_template("views/item.html", item=i)

@main.route("/item/edit/<id>") # edit item
@login_required
def edit_item(id):
    if(current_user.pos == "Producer"):
        i = item.query.filter_by(id=id).first_or_404()
        return render_template("views/edit/item.html", item=i)
    else:
        return redirect(url_for("index"))

@main.route("/item/delete/<id>") # edit item
@login_required
def delete_item(id):
    if(current_user.pos == "Producer"):
        item.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for("admin.profile"))
    else:
        return redirect(url_for("index"))

################# STUDENTS #################
@main.route("/students") # view all students
def view_students():
    students = student.query.all()
    return render_template("views/students.html", students=students)

@main.route("/student/<id>") # view student
def view_student(id):
    s = student.query.filter_by(id=id).first_or_404()
    return render_template("views/student.html", student=s)

@main.route("/student/edit/<id>") # edit item
@login_required
def edit_student(id):
    if(current_user.pos == "Producer"):
        s = student.query.filter_by(id=id).first_or_404()
        return render_template("views/edit/student.html", student=s)
    else:
        return redirect(url_for("index"))

@main.route("/student/delete/<id>") # edit item
@login_required
def delete_student(id):
    if(current_user.pos == "Producer"):
        student.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for("admin.profile"))
    else:
        return redirect(url_for("index"))

############ RESERVATIONS ########################
@main.route("/reservations") # view all reservations
def view_reservations():
    reservations = reservation.query.all()
    return render_template("views/reservations.html", reservations=reservations)

@main.route("/reservation/<id>") # view reservation
def view_reservation(id):
    r = reservation.query.filter_by(id=id).first_or_404()
    return render_template("views/reservation.html", reservation=r)

@main.route("/reservation/edit/<id>") # edit item
@login_required
def edit_reservation(id):
    if(current_user.pos == "Producer"):
        r = reservation.query.filter_by(id=id).first_or_404()
        return render_template("views/edit/reservation.html", reservation=r)
    else:
        return redirect(url_for("index"))

@main.route("/reservation/delete/<id>") # edit item
@login_required
def delete_reservation(id):
    if(current_user.pos == "Producer"):
        reservation.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for("admin.profile"))
    else:
        return redirect(url_for("index"))


@main.route("/log") # view log
def view_log():
    logs = log.query.all()
    return render_template("views/log.html", logs=logs)