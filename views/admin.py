from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from models.models import db,item, student, reservation, log
import pandas as pd
import os
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
    items=item.query.order_by(item.name.asc())
    students=student.query.order_by(student.pos.asc())
    reservations=reservation.query.all()
    return render_template("admin/profile.html.j2", student=current_user, items=items, students=students, reservations=reservations)


@admin.route("new_item", methods=["GET","POST"]) # checkin items
@login_required
def new_item():
    if request.method == "POST":
        name = request.form.get('name')
        item_type = request.form.get('type')
        code = request.form.get('code')

        i = item.query.filter_by(code=code).first() 


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
    i = item.query.filter_by(id=id).first()
    if request.method == "POST":
        name = request.form.get('name')
        item_type = request.form.get('type')
        status = request.form.get('status')
        code = request.form.get('code')

        if name:
            i.name=name
        if item_type:
            i.type=item_type
        if code:
            i.code = code
        if status and i.status == "In":
            i.status = "Out For Maintenance"
            i.status_date = datetime.now()
        elif i.status == "Out For Maintenance":
            i.status = "In"
            i.status_date = datetime.now()
        else:
            flash('Must check item in First!', "Error")

        db.session.commit()
        return redirect(url_for("admin.profile"))


    return render_template("admin/edit_item.html", item=i)


@admin.route("/item/delete/<id>") # delete item
@login_required
def delete_item(id):
    item.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin.profile"))

@admin.route("/student/edit/<id>", methods=["GET","POST"]) # edit student
@login_required
def edit_student(id):
    s = student.query.filter_by(id=id).first()
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('type')
        pos = request.form.get('status')

        if name:
            s.name=name
        if email:
            s.email=email
        if pos:
            s.pos = pos

        db.session.commit()
        return redirect(url_for("admin.profile"))


    return render_template("admin/edit_student.html", student=s)

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

######### IMPORTING ############
@admin.route("item/import", methods=["GET", "POST"])
def import_items():
    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            df = pd.DataFrame(pd.read_csv(file_path))
            df.to_sql("item", db.engine, if_exists='replace', index = False)

    return redirect(url_for("admin.profile"))
