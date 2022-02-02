from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from models.models import db,item, student, reservation, log

"""
############ROUTES##########
admin/ -  parent prefix

profile/ - profile for producers and students
new_item/ - backend for adding items

"""
admin = Blueprint('admin', __name__)

@admin.route("/profile")
@login_required
def profile():
    items=item.query.all()
    students=student.query.all()
    reservations=reservation.query.all()
    return render_template("admin/profile.html", student=current_user, items=items, students=students, reservations=reservations)

@admin.route("new_item", methods=["GET","POST"]) # checkin items
@login_required
def new_item():
    if request.method == "POST":
        name = request.form.get('name')
        item_type = request.form.get('type')
        code = request.form.get('code')

        i = item.query.filter_by(name=name).first() 


        if i:
            flash('item already exists!', "Error")
            return redirect(url_for('main.view_item', id=i.id))

        new_item = item(name=name, type=item_type,code=code, status="In", status_date=datetime.now())

        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for("admin.profile"))

@admin.route("new_student", methods=["GET","POST"]) # checkin items
@login_required
def new_student():
    if request.method == "POST":
        # code to validate and add user to database goes here
        email = request.form.get('email')
        name = request.form.get('name')
        pos = request.form.get('position')
        password = request.form.get('pwd')

        user = student.query.filter_by(email=email).first()

        if user:
            flash('student already exists!', "Error")
            return redirect(url_for('admin.profile'))

        new_user = student(email=email, name=name, pos=pos,pwd=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("admin.profile"))

############# EDITING / DELETING ############
@admin.route("/item/edit/<id>", methods=["GET","POST"]) # edit item
@login_required
def edit_item(id):
    if request.method == "POST":
        name = request.form.get('name')
        item_type = request.form.get('type')
        status = request.form.get('status')
        code = request.form.get('code')

        i = item.query.filter_by(id=id).first()

        if name:
            i.name=name
        if item_type:
            i.type=item_type
        if code:
            i.code = code
        if i.status != status:
            if i.status == "In":
                i.student_id = None
            i.status = status
            i.status_date = datetime.now()

        db.session.commit()
        

    return redirect(url_for("admin.profile"))


@admin.route("/item/delete/<id>") # delete item
@login_required
def delete_item(id):
    item.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin.profile"))

@admin.route("/student/edit/<id>") # edit student
@login_required
def edit_student(id):
    s = student.query.filter_by(id=id).first_or_404()
    return render_template("views/edit/student.html", student=s)

@admin.route("/student/delete/<id>") # delete student
@login_required
def delete_student(id):
    student.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin.profile"))

@admin.route("/reservation/edit/<id>") # edit reservation
@login_required
def edit_reservation(id):
    r = reservation.query.filter_by(id=id).first_or_404()
    return render_template("views/edit/reservation.html", reservation=r)

@admin.route("/reservation/delete/<id>") # delete reservation
@login_required
def delete_reservation(id):
    reservation.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin.profile"))