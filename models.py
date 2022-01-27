from . import db
from flask_login import UserMixin

"""
RELATIONSHIPS
##############

student--->item: One to Many
student--->reservation: One to Many
student--->log: One to Many

item--->reservation: One to Many
item--->log: One to Many

reservation-->log: None

"""

class student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    pos = db.Column(db.String(1000))
    pwd = db.Column(db.String(100))
    items = db.relationship("item", backref="student")
    reservations = db.relationship("reservation", backref="student")
    logs = db.relationship("log", backref="student")
    

class item(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    code = db.Column(db.Integer) 
    name = db.Column(db.String(1000))
    type = db.Column(db.String(1000))
    status_date = db.Column(db.DateTime())
    status = db.Column(db.String(1000))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    logs = db.relationship("log", backref="item")
    reservations = db.relationship("reservation", backref="item")

class reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    student_id = db.Column(db.Integer, db.ForeignKey('student.id')) 
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    date_out = db.Column(db.DateTime())

class log(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    student_id = db.Column(db.Integer, db.ForeignKey('student.id')) 
    item_id = db.Column(db.Integer, db.ForeignKey('item.id')) 
    date_in  = db.Column(db.DateTime())
    date_out = db.Column(db.DateTime())