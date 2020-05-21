from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired,FileAllowed



class searchbox(FlaskForm):
    item = StringField('item')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    dob = StringField('dob', validators = [InputRequired()])
    gender = SelectField('Gender', validators=[InputRequired()], choices=[(0, "Male"), (1, "Female")])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'webp'], 'Image')])
    password = PasswordField('Password', validators=[InputRequired()])