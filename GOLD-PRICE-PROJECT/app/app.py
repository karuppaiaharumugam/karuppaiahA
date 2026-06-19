from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import pickle
import os
import numpy as np
import json
import requests

app = Flask(__name__)
app.secret_key = 'AIzaSyD7ttnURR0SH0-FWmGzKPJq2cPqMuOg_68' 

app.config['UPLOAD_FOLDER'] = 'static/'

# Load prediction model safely
try:
    regressor = pickle.load(open("gold_price_predictor.pkl", "rb"))
except FileNotFoundError:
    print("Warning: gold_price_predictor.pkl not found.")

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return render_template('register.html', error='Username already exists')
        users[username] = {'password': password}
        save_users(users)
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('Home.html')
    return redirect(url_for('login'))

@app.route('/market-rates')
def market_rates():
    if 'username' in session:
        return render_template('gold.html')
    return redirect(url_for('login'))

@app.route('/goldr')
def goldr():
    if 'username' in session:
        return render_template('GoldR.html')
    return redirect(url_for('login'))

@app.route("/index", methods=['GET', 'POST'])
def index_page():
    if 'username' in session:
        picl = os.path.join(app.config['UPLOAD_FOLDER'], 'gold.jpg')
        return render_template("index.html", gold_pic=picl)
    return redirect(url_for('login'))

@app.route("/display", methods=['POST'])
def display():
    try:
        SPX = float(request.form["SPX"])
        USO = float(request.form["USO"])
        SLV = float(request.form["SLV"])
        EUR_USD = float(request.form["EUR_USD"])
        input_data = np.asarray((SPX, USO, SLV, EUR_USD)).reshape(1,-1)
        prediction = regressor.predict(input_data)[0]
        result = "{:.2f}".format(prediction)
        picl = os.path.join(app.config['UPLOAD_FOLDER'], 'gold.jpg')
        return render_template("display.html", result=result, gold_pic=picl)
    except Exception as e:
        return f"Error: {str(e)}"



if __name__ =='__main__':
   app.run(debug=True, port=8888)