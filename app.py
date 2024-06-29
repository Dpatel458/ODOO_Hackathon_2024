# app.py
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import requests
import mysql.connector
from auth import register_user, authenticate_user
from recommendation import get_recommendations
from user_profile import get_user_profile, update_user_profile
from diet_plans import create_meal_plan, get_meal_plan
from nutritional_db import add_food, search_foods
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

APP_ID = '0a0a693e'
API_KEY = '***' ## Sorry as GitHub is not allowing secret API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['user_id']
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        dietary_preferences = request.form['dietary_preferences']
        allergies = request.form['allergies']
        health_goals = request.form['health_goals']
        update_user_profile(user_id, age, gender, weight, height, dietary_preferences, allergies, health_goals)
    user_profile = get_user_profile(session['username'])
    return render_template('profile.html', profile=user_profile)

from datetime import datetime

@app.route('/meal_plan', methods=['GET'])
def meal_plan():
    user_id = session['user_id']
    plan_date_str = request.args.get('plan_date', '')
    try:
        plan_date = datetime.strptime(plan_date_str, '%Y-%m-%d').date()
    except ValueError:
        plan_date = datetime.today().date()  
    meal_plans = get_meal_plan(user_id, plan_date)
    return render_template('meal_plan.html', meal_plans=meal_plans)

@app.route('/foods', methods=['GET', 'POST'])
def foods():
    if request.method == 'POST':
        name = request.form['name']
        calories = request.form['calories']
        protein = request.form['protein']
        fat = request.form['fat']
        carbs = request.form['carbs']
        vitamins = request.form['vitamins']
        minerals = request.form['minerals']
        add_food(name, calories, protein, fat, carbs, vitamins, minerals)
    foods = search_foods(request.args.get('query', ''))
    return render_template('foods.html', foods=foods)


@app.route('/recommendations', methods=['POST'])
def recommendations():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_profile = get_user_profile(session['user_id'])
    if user_profile is None:
        return "User profile not found", 404
    
    query_params = {
        'appId': APP_ID,
        'appKey': API_KEY,
        'query': 'meal',           
        'cal_min': 300,              
        'cal_max': 600,            
        'fields': 'item_name,nf_calories,nf_protein,nf_total_fat,nf_total_carbohydrate,nf_sodium',  
        'sort': 'r',               
        'limit': 10                 
    }
    

    try:
        response = requests.get('https://api.nutritionix.com/v1_1/search/', params=query_params)
        response.raise_for_status()

        data = response.json()
        hits = data.get('hits', [])

        recommendations = []
        for hit in hits:
            item = hit['fields']
            recommendations.append({
                'label': item['item_name'],
                'calories': int(item['nf_calories']),
                'protein': int(item['nf_protein']),
                'fat': int(item['nf_total_fat']),
                'carbs': int(item['nf_total_carbohydrate']),
                'sodium': int(item['nf_sodium'])
            })

        return render_template('recommendations.html', recommendations=recommendations)

    except requests.exceptions.RequestException as e:
        print(f"Error accessing Nutritionix API: {e}")
        return "Error accessing Nutritionix API", 500





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
