from flask import Blueprint, current_app, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app.forms.auth_valid import LoginForm, RegistrationForm
from app.models.user import User
from app.extensions import params

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.admin'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Find user by username or email
            user = User.query.filter(
                (User.username == form.username.data) | 
                (User.email == form.username.data)
            ).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('user.admin'))
            else:
                flash('Invalid username or password', 'danger')
        except Exception as e:
            current_app.logger.error(f"Error during login: {e}")
            flash('An error occurred during login. Please try again.', 'danger')
    return render_template("login.html", params=params, form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.admin'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            if form.confirm_password.data != form.password.data:
                raise ValueError("Passwords do not match")
            
            user = User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            if not user:
                raise ValueError("Failed to create user")
            login_user(user)
            return redirect(url_for('user.admin'))
        except Exception as e:
            flash(f'An error occurred during registration {e}. Please try again.', 'danger')
    return render_template("register.html", params=params, form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/auth/login")