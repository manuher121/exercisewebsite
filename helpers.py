import requests
import sqlite3
from flask import redirect, render_template, session
from functools import wraps
from sqlalchemy import select, create_engine, insert
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session, render_template, redirect



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    def escape(s):
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
            ]:
            s = s.replace(old, new)
            return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_info_db(engine, Exercise):
    get_exercises_info = select(Exercise).where(Exercise.user_id == session["user_id"])
    with engine.connect() as conn:
        result = conn.execute(get_exercises_info)
        for row in result:
            exercises_info = row._mapping
            return exercises_info