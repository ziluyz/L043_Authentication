from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask import flash

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ChangeDataForm(FlaskForm):
    username = StringField('Username')
    change_username = BooleanField('Change username')
    
    email = StringField('Email')
    change_email = BooleanField('Change email')
    
    new_password = PasswordField('New password')
    change_password = BooleanField('Change password')
    
    confirm_new_password = PasswordField('Confirm new password', validators=[EqualTo('new_password')])
    
    current_password = PasswordField('Enter current password', validators=[DataRequired()])
    
    submit = SubmitField('Confirm changes')
    
    def validate(self, extra_validators=None):
        # Call the parent class's validate method
        if not super(ChangeDataForm, self).validate(extra_validators):
            return False
        # Custom validation logic
        if self.change_username.data:
            if not self.username.data:
                self.username.errors.append('Username is required if changing username.')
                return False
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                self.username.errors.append('That username is taken. Please choose a different one.')
                return False
        
        if self.change_email.data:
            if not self.email.data:
                self.email.errors.append('Email is required if changing email.')
                return False
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                self.email.errors.append('That email is taken. Please choose a different one.')
                return False
        
        if self.change_password.data:
            if not self.new_password.data:
                self.new_password.errors.append('New password is required if changing password.')
                return False
        
        return True