from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,EqualTo,Length,ValidationError
from modules import *

def invalid_credentials(form,field) :

    password=field.data
    username=form.username.data 

    user=User.query.filter_by(username=username).first()

    if user is None :
        raise ValidationError("Username or Password is incorrect")

    elif password != user.password :
        raise ValidationError("Username or password is incorrect")

class registration(FlaskForm):
    # regestration
    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])

    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])

    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])  
    
    
    
    def validate_username(self,username) :
         user_ob=User.query.filter_by(username=username.data).first()
         if user_ob :
             raise ValidationError("username already exist")

    
class loginform(FlaskForm) :

    username=StringField('username',validators=[InputRequired(message="User name required")])
    password=PasswordField('password',validators=[InputRequired(message="password required"),invalid_credentials])



