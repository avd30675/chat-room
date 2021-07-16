from flask import Flask,render_template,url_for
from forms import *

app=Flask(__name__)

app.secret_key='replace later'



@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = registration()

    # Update database if validation success
    if reg_form.validate_on_submit():
        return "thank you"
        

    return render_template("register.html", form=reg_form)

if __name__=='__main__' :

    app.run(debug=True)