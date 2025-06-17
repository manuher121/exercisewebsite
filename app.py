from flask import Flask, request, session
from flask import render_template
from helpers import login_required
from flask_session import Session

app = Flask(__name__)   

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@login_required 
def index():
    return render_template('layout.html')



@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()












#@app.route("/register", method=["GET", "POST"])
#def register():
    #register user