from datetime import datetime
from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash
from . import db
from .models import item, reservation, student

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

reserve = Blueprint('reserve', __name__)

@reserve.route("add", methods=["GET", "POST"]) # reserve items
def add_reservation():
    if request.method == "POST":
        name = request.form.get("name", type=str)
        date = request.form.get("date", type=str)
        date = datetime.fromisoformat(date)

        ids = request.form.get("ids")
        ids = ids.split(",")

        s = student.query.filter_by(name=name).first()

        for id in ids:
            new_reservation = reservation(student_id=s.id, item_id=id, date_out=date)
            db.session.add(new_reservation)
            db.session.commit()

        check_reservation()

        return redirect(url_for("index"))

    students = student.query.all()
    items = item.query.all()
    return render_template("reserve/new.html", students=students, items=items)

@reserve.route("change", methods=["GET", "POST"]) # change reservation
def edit_reservation():
    # TODO change reservation logic
    pass

def check_reservation():
    with db.app.app_context():
        reservations = reservation.query.all()

        for r in reservations:
            if r.date_out.date() == datetime.now().date:
                i = item.query.filter_by(id=r.item_id).first()
                i.status="Reserved"
                i.student_id = r.student_id
                i.status_date = datetime.now()
                reservation.query.filter_by(id=r.id).delete()
                db.session.commit()
                print("Updating Reservation")

@reserve.route("check_new_reservation", methods=["GET"]) # backend reservation
def check_new_reservation():
    with db.app.app_context():
        date = request.args.get("date", type=str)
        date = datetime.fromisoformat(date)
        reservations = reservation.query.all()

        items = []

        for r in reservations:
            day = r.date_out
            if day.day == date.day:
                i = item.query.filter_by(id=r.item_id).first()
                items.append(i.id)
        
        return jsonify(items)



scheduler = BackgroundScheduler()
scheduler.add_job(func=check_reservation, trigger="interval", seconds=60)
scheduler.start()


atexit.register(lambda: scheduler.shutdown())
