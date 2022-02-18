from datetime import datetime
from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash
from sqlalchemy import and_
from src.models.models import db, item, reservation, student

reserve = Blueprint('reserve', __name__)


@reserve.route("add", methods=["GET", "POST"])  # reserve items
def add_reservation():
    if request.method == "POST":
        name = request.form.get("name", type=str)
        date = request.form.get("date", type=str)
        date = datetime.fromisoformat(date)

        ids = request.form.get("ids")
        ids = ids.split(",")

        s = student.query.filter_by(name=name).first()

        new_reservations = []
        if ids:
            ids = list(set(ids))
            for id in ids:
                if not is_reserved(id, date):
                    new_reservations.append(reservation(
                        student_id=s.id, item_id=id, date_out=date))
                else:
                    i = item.query.filter_by(id=id).first()
                    flash(i.name + " already reserved!", "Error")
                    return redirect(url_for("index"))

            for r in new_reservations:
                db.session.add(r)
            db.session.commit()

        return redirect(url_for("index"))

    students = student.query.all()
    items = item.query.all()
    return render_template("reserve/new.html", students=students, items=items)


def is_reserved(i, date):
    print(i)
    with db.app.app_context():
        reservations = db.session.query(reservation).filter(
            and_(reservation.date_out == date, reservation.item_id==i)).first()
        if reservations:
            return True

@reserve.route("check_new_reservation", methods=["GET"])  # backend reservation
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
