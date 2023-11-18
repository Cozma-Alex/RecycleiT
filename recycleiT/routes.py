import os
import uuid

from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from database import *
from server import app
from models import User
from forms import RegisterForm, LoginForm
from __init__ import bcrypt

from __init__ import app


@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')


@app.route("/leaderboard")
def leaderboard():
    return "Leaderboard"


@app.route('/profile')
@login_required
def about():
    #rows = get_all()
    items = [User(id=row[0], firstName=row[1], lastName=row[2], username=row[3], email=row[4], password=row[5], totalPoints=row[6]) for row in rows]
    return render_template('profile.html', items=items)

@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/map')
def maps():
    return render_template('map.html')


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = get_user_by_username(usernameToCheck=form.username.data)
        if attempted_user is not None and bcrypt.check_password_hash(attempted_user.get_password(), form.password.data):
            login_user(attempted_user)
            flash(f'Succes! You are logged in as:{attempted_user.username}', category='success')
            return redirect(url_for('about'))
        else:
            flash('Username and password are not match! Try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/register')
def register():
    return 'Register'


if __name__ == "__main__":
    if not os.environ.get('IS_CONTAINER'):
        app.run(debug=True, port=8080)
    else:
        port = os.environ.get('PORT')
        if port is None:
            port = '8080'
        app.run(host=f'0.0.0.0:{port}')
