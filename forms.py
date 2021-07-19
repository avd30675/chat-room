from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,EqualTo,Length,ValidationError
from modules import *


class registration(FlaskForm):
    # regestration
    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])

    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])

    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])  
    
    
    
    def validate_username(self,username) :
         user_ob=User.query.filter_by(username=username.data).first()
         if user_ob :
             raise ValidationError("username already exist")

    
    


