from . import db
from flask_login import UserMixin
from datetime import datetime
import pytz
from tzlocal import get_localzone

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(500))
    cals = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def local_time(self):
        return self.date.replace(tzinfo=pytz.utc).astimezone(get_localzone())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(25))
    meals = db.relationship('Meal')

    @property
    def total_macros(self):
        cur_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(get_localzone())
        totals = [0, 0, 0, 0]
        for meal in self.meals:
            if meal.local_time.year == cur_time.year and meal.local_time.month == cur_time.month and meal.local_time.day == cur_time.day:
                totals[0] += meal.cals
                totals[1] += meal.protein
                totals[2] += meal.carbs
                totals[3] += meal.fat
        return totals
    @property
    def average_macros(self):
        averages = [0, 0, 0, 0]
        totals = [0, 0, 0, 0]
        prev_days = []
        for meal in self.meals:
            totals[0] += meal.cals
            totals[1] += meal.protein
            totals[2] += meal.carbs
            totals[3] += meal.fat
            new_day = True
            for prev_day in prev_days:
                if meal.local_time.year == prev_day.year and meal.local_time.month == prev_day.month and meal.local_time.day == prev_day.day:
                    new_day = False
            if new_day:
                prev_days.append(meal.local_time)
        num_days = len(prev_days)
        if num_days > 0:
            averages = [totals[0]//num_days, totals[1]//num_days, totals[2]//num_days, totals[3]//num_days]
        return averages
