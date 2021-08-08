from flask import Flask,render_template,url_for,redirect,flash
from forms import *
from modules import *
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user,login_required, logout_user
from flask_socketio import SocketIO,send, emit ,join_room,leave_room
import time

app=Flask(__name__)

app.config['SECRET_KEY']="secreat"
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

#configuration of database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xfwrmdhryawaql:e3a13e6544bb1423b66553abb91f75caff2ed6ee99b099891d607febdc113792@ec2-35-171-250-21.compute-1.amazonaws.com:5432/d6tm7teu5j5cnc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

#login maneger intialization
login=LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id) :
     return User.query.get(int(id))

#---------------------------------------------------------------------------------
#rooms-----------
ROOMS=["c++","python","javascript"]

#intialise 
socketio = SocketIO(app,manage_session=False)

@socketio.on('message')
def on_message(data):
    """Broadcast messages"""

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Set timestamp
    print(msg)
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)



@socketio.on('join')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    print(username + " has joined the ")
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    username = data['username']
    room = data['room']
    leave_room(room)
    print(username + " has left the room")
    send({"msg": username + " has left the room"}, room=room)
    



#---------------------------------------------------------------------------------------



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
        flash("Registered successfull please login",'success')
        return redirect(url_for('login'))
    
    return render_template("register.html", form=reg_form)

@app.route("/login",methods=['GET','POST']) 
def login() :

    login_form=loginform()
    if login_form.validate_on_submit() :
        user_obj=User.query.filter_by(username=login_form.username.data).first()
        login_user(user_obj)
        if current_user.is_authenticated  :
              return redirect(url_for('chat'))
        else :
            return "not login"
    
    return render_template("login.html",form=login_form)

@app.route("/logout", methods=['GET'])
def logout():

    # Logout user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route("/chat",methods=['GET','POST'])
#@login_required
def chat():

    if not current_user.is_authenticated:
        flash('please login befor chat','danger')
        return redirect(url_for('login'))
    return render_template('chat.html',username=current_user.username,rooms=ROOMS)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__=='__main__' :

    socketio.run(app,debug=True)