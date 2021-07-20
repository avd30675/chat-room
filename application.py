from flask import Flask,render_template,url_for,redirect
from forms import *
from modules import *
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user,login_required, logout_user



app=Flask(__name__)

app.secret_key='replace later'

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xfwrmdhryawaql:e3a13e6544bb1423b66553abb91f75caff2ed6ee99b099891d607febdc113792@ec2-35-171-250-21.compute-1.amazonaws.com:5432/d6tm7teu5j5cnc'

db=SQLAlchemy(app)

login=LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id) :
     return User.query.get(int(id))






@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = registration()

    # Update database if validation success
    if reg_form.validate_on_submit():
        
        username=reg_form.username.data 
        password=reg_form.password.data 
        
        hashed_password=pbkdf2_sha256.hash(password)
 
        user=User(username=username,password=hashed_password) 
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template("register.html", form=reg_form)

@app.route("/login",methods=['GET','POST']) 
def login() :

    login_form=loginform()
    if login_form.validate_on_submit() :
        user_obj=User.query.filter_by(username=login_form.username.data).first()
        login_user(user_obj)
        if current_user.is_authenticated  :
              return "Logged in !"
        else :
            return "not login"
    
    return render_template("login.html",form=login_form)



@app.route("/chat",methods=['GET','POST'])
#@login_required
def chat():

    if not current_user.is_authenticated:
        return "please login before chat" 
    return "chat with me"


@app.route("/logout",methods=['GET'])
@login_required
def logout() :

    logout_user()
    return "logged out using flask_login"


if __name__=='__main__' :

    app.run(debug=True)