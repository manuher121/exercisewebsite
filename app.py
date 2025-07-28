import os
from datetime import datetime
from flask import Flask, request, session, render_template, redirect
from helpers import login_required, apology, dict_factory, get_info_db
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


class Exercise(db.Model):
    __tablename__ = 'exercises'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    sit_ups = db.Column(db.Integer)
    push_ups = db.Column(db.Integer)
    plank = db.Column(db.Integer)
    run = db.Column(db.Float)
    money_spent = db.Column(db.Float)
    weight = db.Column(db.Integer)
    healthy_food = db.Column(db.Integer)
    time = db.Column(db.String)

class Daily(db.Model):
    __tablename__ = "daily"
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    sit_ups = db.Column(db.Integer)
    push_ups = db.Column(db.Integer)
    plank = db.Column(db.Integer)
    run = db.Column(db.Float)
    money_spent = db.Column(db.Float)
    weight = db.Column(db.Integer)
    healthy_food = db.Column(db.String)
    time = db.Column(db.String)


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

    user_info = get_info_db(engine, Exercise)
    try:
        if user_info.user_id == session["user_id"]:
            date = datetime.now()
            exercise_check = get_info_db(engine, Daily)
        try:
            if (exercise_check.time == date.strftime('%d/%m/%Y')):
                return apology("you did it already", 400)
            else:
                return redirect("/daily")
        except:
            return redirect("/daily")
    except:                            
        return render_template("options.html")

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


@app.route("/options")
def options():
    
    return apology("No options to add", 300)

@app.route("/daily", methods=["GET", "POST"])
def daily(): 

    if request.method == "POST":
        info = get_info_db(engine, Exercise)
        if not request.form.get("sit_ups"):
            return apology("Do the sit ups!", 300)
        if not request.form.get("push_ups"):
            return apology("Do the Push-Ups!", 300)
        if not request.form.get("plank"):
            return apology("Do the Planks!", 300)
        if not request.form.get("run"):
            return apology("RUN!", 300)
        if not request.form.get("amount"):
            return apology("Enter an amount!", 300)
        if not request.form.get("weight"):
            return apology("Enter your weight!", 300)
        
        date = datetime.now()
        daily_exercise = insert(Daily).values(user_id = session["user_id"], sit_ups = info.sit_ups, push_ups = info.push_ups, 
                                                  plank = info.plank, run = info.run, money_spent = request.form.get("amount"), 
                                                  weight = request.form.get("weight"), healthy_food = request.form.get("food"), time=date.strftime('%d/%m/%Y'))
        with engine.connect() as conn:
            result = conn.execute(daily_exercise)
            conn.commit()
        return apology("user already in use", 400)

    user_info = get_info_db(engine, Exercise)
    try:
        if user_info.user_id == session["user_id"]:
            date = datetime.now()
            exercise_check = get_info_db(engine, Daily)
            try:
                if (exercise_check.time == date.strftime('%d/%m/%Y')):
                    return apology("you did it already", 400)
                else:
                    return render_template("daily.html",info=user_info, date=date.strftime('%d/%m/%Y %H:%M'))
            except:
                return render_template("daily.html",info=user_info, date=date.strftime('%d/%m/%Y %H:%M'))
        else:                            
            return redirect("/options")
    except:
        return redirect("/options")