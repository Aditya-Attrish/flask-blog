# app/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Optional, URL, ValidationError
import re

class ProfileForm(FlaskForm):
    # Personal Information
    first_name = StringField('First Name', validators=[
        Length(max=50, message='First name must be less than 50 characters')
    ])

    last_name = StringField('Last Name', validators=[
        Length(max=50, message='Last name must be less than 50 characters')
    ])

    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])

    location = StringField('Location', validators=[
        Length(max=100, message='Location must be less than 100 characters')
    ])

    website = StringField('Website', validators=[
        Optional(),
        URL(message='Please enter a valid URL'),
        Length(max=200, message='Website URL must be less than 200 characters')
    ])

    # Social Links
    twitter_url = StringField('Twitter URL', validators=[
        Optional(),
        URL(message='Please enter a valid URL'),
        Length(max=200, message='Twitter URL must be less than 200 characters')
    ])

    linkedin_url = StringField('LinkedIn URL', validators=[
        Optional(),
        URL(message='Please enter a valid URL'),
        Length(max=200, message='LinkedIn URL must be less than 200 characters')
    ])

    github_url = StringField('GitHub URL', validators=[
        Optional(),
        URL(message='Please enter a valid URL'),
        Length(max=200, message='GitHub URL must be less than 200 characters')
    ])

    instagram_url = StringField('Instagram URL', validators=[
        Optional(),
        URL(message='Please enter a valid URL'),
        Length(max=200, message='Instagram URL must be less than 200 characters')
    ])

    # Avatar
    avatar = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])

    # Preferences
    newsletter = BooleanField('Subscribe to newsletter')
    public_profile = BooleanField('Make profile public')
    email_notifications = BooleanField('Email notifications')

    submit = SubmitField('Update Profile')

    def validate_twitter_url(self, field):
        if field.data and 'twitter.com' not in field.data and 'x.com' not in field.data:
            raise ValidationError('Please enter a valid Twitter URL')

    def validate_linkedin_url(self, field):
        if field.data and 'linkedin.com' not in field.data:
            raise ValidationError('Please enter a valid LinkedIn URL')

    def validate_github_url(self, field):
        if field.data and 'github.com' not in field.data:
            raise ValidationError('Please enter a valid GitHub URL')

    def validate_instagram_url(self, field):
        if field.data and 'instagram.com' not in field.data:
            raise ValidationError('Please enter a valid Instagram URL')