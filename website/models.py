from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(500))
    cals = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(25))
    meals = db.relationship('Meal')
