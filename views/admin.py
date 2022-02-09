from datetime import datetime
from operator import index
from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from models.models import db,item, student, reservation, log
import pandas as pd
import os
from sqlalchemy.exc import IntegrityError

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

@admin.route("/items")
@login_required
def admin_items():
    items=item.query.order_by(item.name.asc())
    return render_template("admin/items.html", student=current_user, items=items)

@admin.route("/students")
@login_required
def admin_students():
    students=student.query.order_by(student.pos.asc())
    return render_template("admin/students.html", student=current_user, students=students)

@admin.route("/reservations")
@login_required
def admin_reservations():
    reservations=reservation.query.all()
    return render_template("admin/reservations.html", student=current_user, reservations=reservations)

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

        return redirect(url_for("admin.admin_items"))

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
            return redirect(url_for('admin.admin_students'))

        new_user = student(email=email, name=name, pos=pos,pwd=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("admin.admin_students"))

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
        elif i.status != "In" and status:
            flash('Must check item in first!', "Error")

        try:
            db.session.commit()
        except IntegrityError:
            flash('Edit conflicts with other items!', "Error")


        return redirect(url_for("admin.admin_items"))


    return render_template("admin/edit_item.html", item=i)


@admin.route("/item/delete/<id>") # delete item
@login_required
def delete_item(id):
    item.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin.admin_items"))

@admin.route("/student/edit/<id>", methods=["GET","POST"]) # edit student
@login_required
def edit_student(id):
    s = student.query.filter_by(id=id).first()
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        pos = request.form.get('status')

        if name:
            s.name=name
        if email:
            s.email=email
        if pos:
            s.pos = pos

        db.session.commit()
        return redirect(url_for("admin.admin_students"))


    return render_template("admin/edit_student.html", student=s)

@admin.route("/student/delete/<id>") # delete student
@login_required
def delete_student(id):
    student.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin.admin_students"))

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
    return redirect(url_for("admin.admin_reservations"))\

######### IMPORTING ############
@admin.route("item/import", methods=["GET", "POST"])
@login_required
def import_items():
    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            df = pd.DataFrame(pd.read_csv(file_path))
            try:
                df.to_sql("item", db.engine, if_exists='append', index = False)
            except IntegrityError:
                flash("Codes already in database!", "Error")

    return redirect(url_for("admin.admin_items"))

######### EXPORTING ############
@admin.route("item/export")
@login_required
def export_items():
    df = pd.read_sql(item.query.statement, db.engine).drop("id", axis=1)
    csv = df.to_csv(index=False)  
    response = make_response(csv)
    cd = 'attachment; filename=item.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response