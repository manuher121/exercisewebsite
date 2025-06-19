import os
from flask import Flask, request, session, render_template, redirect
from helpers import login_required, apology
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, create_engine, insert
from werkzeug.security import check_password_hash, generate_password_hash


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

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
@login_required 
def index():
    return render_template('layout.html')


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    
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
        try:
            if check_password_hash(new_result.hash, request.form.get("password")):
                session["user_id"] =  new_result.id
                return redirect("/")
            else:
                return apology("incorrect password", 403)
        except: 
            return apology("incorrect username", 403)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    #register user

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide a username", 400)
        if not request.form.get("email"):
            return apology("must provide a email", 400)
        if not request.form.get("password"):
            return apology("must provide a password", 400)
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match", 400)

        try:
            current_user = insert(User).values(username = (request.form.get("username")), hash = (generate_password_hash(request.form.get("password"), 
                                            method='scrypt', salt_length=16)), email = (request.form.get("email")))

            with engine.connect() as conn:
                result = conn.execute(current_user)
                conn.commit()
        except:
            return apology("user already in use", 400)

        return redirect("/")
    else:
        return render_template("register.html")









@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")