from flask import Flask, request, session, render_template, redirect
from helpers import login_required, apology
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, create_engine
import os

app = Flask(__name__)   


# Route of the DB, initiliaze it
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine("sqlite:///database.db")

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@login_required 
def index():
    return render_template('layout.html')



@app.route("/login", methods=["GET", "POST"])
def login():


    
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must give a username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        


        current_user = select(User).where(User.username == (request.form.get("username")))
        with engine.connect() as conn:
            result = conn.execute(current_user)
            for row in result:
                new_result = row

        #if current_user.hash == request.form.get("password"):
        #   session["user_id"] =  current_user.id
        #else:
        #    return apology("incorrect password", 403)

        return render_template("login.html", user = new_result.hash)


    else:
        return render_template("login.html")


#@app.route("/register", method=["GET", "POST"])
#def register():
    #register user