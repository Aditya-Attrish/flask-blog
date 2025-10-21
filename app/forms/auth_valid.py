# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField(
        'Username or Email',
        validators=[
            DataRequired(message='Username or email is required'),
            Length(min=3, max=64)
        ])

    password = PasswordField('Password',
                             validators=[
                                 DataRequired(message='Password is required'),
                                 Length(min=8, max=24)
                             ])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3,
                   max=64,
                   message='Username must be between 3 and 64 characters')
        ])

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Please enter a valid email address'),
            Length(max=120)
        ])

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8,
                   max=24,
                   message='Password must be at least 8 characters long')
        ])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired()])

    # Preferences
    newsletter = BooleanField('Subscribe to newsletter', default=True)
    terms = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[
        DataRequired(message='You must agree to the terms and conditions')
    ])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Email already registered. Please use a different email.')

    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords must match.')
