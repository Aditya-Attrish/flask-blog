from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user
from app.models.user import User
from app.extensions import db, params

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pas = request.form['password']
        remember = request.form.get('remember', '')

        usern = User.query.filter_by(username=user).first()
        if usern and usern.check_password(pas):
            login_user(usern, remember=remember == "on")
            return redirect('/user')
    return render_template("login.html", params=params)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form['emailId']
        usern = request.form['username']
        pas = request.form['password']
        remember = request.form['remember']
        confirm_password = request.form['confirm_password']

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=usern).first()
        if existing_user:
            flash(
                'Username already taken. Please choose a different username.',
                'danger')
            return redirect('/register')

        if pas != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect('/register')

        user = User(email=email, username=usern, password=pas)
        # Hashing a password
        user.password = user.set_password(pas)
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=remember == "on")
        return redirect('/user')
    return render_template("register.html", params=params)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/auth/login")