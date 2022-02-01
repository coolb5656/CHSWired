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