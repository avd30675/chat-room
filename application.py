from flask import Flask,render_template,url_for
from forms import *
from modules import *


app=Flask(__name__)

app.secret_key='replace later'

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xfwrmdhryawaql:e3a13e6544bb1423b66553abb91f75caff2ed6ee99b099891d607febdc113792@ec2-35-171-250-21.compute-1.amazonaws.com:5432/d6tm7teu5j5cnc'

db=SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = registration()

    # Update database if validation success
    if reg_form.validate_on_submit():
        
        username=reg_form.username.data 
        password=reg_form.password.data 


        user=User(username=username,password=password) 
        db.session.add(user)
        db.session.commit()

        return "user created"




        

    return render_template("register.html", form=reg_form)

if __name__=='__main__' :

    app.run(debug=True)