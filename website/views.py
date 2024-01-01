from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Meal
from . import db
import json
import re
from datetime import datetime
import pytz
from tzlocal import get_localzone

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        desc = request.form.get('desc')
        cals = request.form.get('cals')
        protein = request.form.get('protein')
        carbs = request.form.get('carbs')
        fat = request.form.get('fat')

        if len(desc) < 1:
            flash('Meal description must be at least 1 character long.', category='error')
        elif len(desc) > 500:
            flash('Meal description must be at most 500 characters long.', category='error')
        elif len(cals) < 1:
            flash('Calorie count must be at least 1 digit long.', category='error')
        elif len(cals) > 4:
            flash('Calorie count must be at most 4 digits long.', category='error')
        elif not (re.search("^[0-9]+$", cals)):
            flash('Calorie count must be a non-negative number.', category='error')
        elif len(protein) < 1:
            flash('Protein count must be at least 1 digit long.', category='error')
        elif len(protein) > 3:
            flash('Protein count must be at most 3 digits long.', category='error')
        elif not (re.search("^[0-9]+$", protein)):
            flash('Protein count must be a non-negative number.', category='error')
        elif len(carbs) < 1:
            flash('Carbohydrate count must be at least 1 digit long.', category='error')
        elif len(carbs) > 3:
            flash('Carbohydrate count must be at most 3 digits long.', category='error')
        elif not (re.search("^[0-9]+$", carbs)):
            flash('Carbohydrate count must be a non-negative number.', category='error')
        elif len(fat) < 1:
            flash('Fat count must be at least 1 digit long.', category='error')
        elif len(fat) > 3:
            flash('Fat count must be at most 3 digits long.', category='error')
        elif not (re.search("^[0-9]+$", fat)):
            flash('Fat count must be a non-negative number.', category='error')
        else:
            new_meal = Meal(desc=desc, cals=cals, protein=protein, carbs=carbs, fat=fat, user_id=current_user.id)
            db.session.add(new_meal)
            db.session.commit()
            flash('Meal added!', category='success')

    return render_template("home.html", user=current_user, cur_time=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(get_localzone()))

@views.route('/delete-meal', methods=['POST'])
def delete_meal():
    meal = json.loads(request.data)
    mealId = meal['mealId']
    meal = Meal.query.get(mealId)
    if meal:
        if meal.user_id == current_user.id:
            db.session.delete(meal)
            db.session.commit()
    flash('Meal deleted!', category='success')
    
    return jsonify({})

@views.route('/reset-totals', methods=['POST'])
def reset_totals():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    cur_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(get_localzone())
    if user:
        for meal in user.meals:
            if meal.local_time.year == cur_time.year and meal.local_time.month == cur_time.month and meal.local_time.day == cur_time.day:
                db.session.delete(meal)
        db.session.commit()
    flash('Totals have been reset!', category='success')
    
    return jsonify({})

@views.route('/reset-averages', methods=['POST'])
def reset_averages():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    cur_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(get_localzone())
    if user:
        for meal in user.meals:
            if meal.local_time.year != cur_time.year and meal.local_time.month != cur_time.month and meal.local_time.day != cur_time.day:
                db.session.delete(meal)
        db.session.commit()
    flash('Averages have been reset!', category='success')
    
    return jsonify({})
