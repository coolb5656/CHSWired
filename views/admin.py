from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.models import db,item, student, reservation, log

admin = Blueprint('admin', __name__)

@admin.route("/profile")
@login_required
def profile():
    if(current_user.pos == "Producer"):
        items=item.query.all()
        students=student.query.all()
        reservations=reservation.query.all()
        return render_template("admin/profile.html", student=current_user, items=items, students=students, reservations=reservations)
    return redirect(url_for('main.view_student', id=current_user.id))

@admin.route("new_item", methods=["GET","POST"]) # checkin items
@login_required
def checkin_item():
    if(current_user.pos == "Producer"):
        if request.method == "POST":
            name = request.form.get('name')
            item_type = request.form.get('type')
            code = request.form.get('code')

            i = item.query.filter_by(name=name).first() # if this returns a user, then the email already exists in database


            if i: # if a user is found, we want to redirect back to signup page so user can try again
                flash('item already exists!')
                return redirect(url_for('main.view_item', id=i.id))

            new_item = item(name=name, type=item_type,code=code, status="In", status_date=datetime.now())

            db.session.add(new_item)
            db.session.commit()

            return redirect(url_for("admin.profile"))

        names = student.query.all()
        return render_template("checkout/checkin.html", names=names)