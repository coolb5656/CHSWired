from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import item, student
from flask import jsonify

checkout = Blueprint('checkout', __name__)

@checkout.route("checkout", methods=["GET", "POST"]) # checkin items
def checkout_item():
    if request.method == "POST":
        name = request.form.get("name")
        ids = request.form.get("ids")
        ids = ids.split(",")

        s = student.query.filter_by(name=name).first()

        for id in ids:
            i = item.query.filter_by(id=id).first()                
            i.status="Out"
            i.status_date = datetime.now()
            i.student_id = s.id
            db.session.commit()

        return redirect(url_for("index"))

    names = student.query.all()
    return render_template("checkout/checkout.html", names=names)

@checkout.route("checkin", methods=["GET", "POST"]) # checkin items
def checkin_item():
    if request.method == "POST":
        ids = request.form.get("ids")
        ids = ids.split(",")

        for id in ids:
            i = item.query.filter_by(id=id).first()                
            i.status="In"
            i.status_date = datetime.now()
            i.student_id = None
            db.session.commit()

        return redirect(url_for("index"))

    names = student.query.all()
    return render_template("checkout/checkin.html", names=names)

@checkout.route("scan", methods=["GET"]) # backend for returning item names
def scan():
    code = request.args.get("code", type=str)
    if code:
        i = item.query.filter_by(code=code).first()
        if i is None:
            return jsonify(id=0, status="Non Existent", name="ERROR")

    return jsonify(id=i.id, status=i.status, name=i.name)

@checkout.route("scan_name", methods=["GET"]) # backend for returning item names
def scan_name():
    name = request.args.get("name", type=str)
    if name:
        i = item.query.filter_by(name=name).first()
        if i is None:
            return jsonify(id=0, status="Non Existent", name="ERROR")

    return jsonify(id=i.id, status=i.status, name=i.name)