import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
import sqlite3
from sqlite3 import Error
import string
import random
import json
import pyttsx3
from gtts import gTTS
import codecs
from mutagen.mp3 import MP3
import re

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

def queryDB(query, vals = ()):
    myConn = create_connection(r"/mnt/c/Users/aepst/Documents/Projects/Project4/proj4.db")
    myConn.row_factory = sqlite3.Row
    cur = myConn.cursor()
    cur.execute(query, vals)
    myConn.commit()
    answer = cur.fetchall()
    myConn.close()
    return answer

allCategories = ["Current Events", "Fine Arts", "Geography", "History", "Literature", "Mythology", "Philosophy", "Religion", "Science", "Social Science", "Trash"]

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        categories = request.form.get("categories").split(",")
        if len(categories) == 1 and categories[0] == '':
            print(categories)
            categories = [str(i) for i in range(len(allCategories))]
        
        qContains = request.form.get("qWords").split(",")
        aContains = request.form.get("aWords").split(",")
        qContains = ["%" + q.strip().lower() + "%" for q in qContains]
        aContains = ["%" + a.strip().lower() + "%" for a in aContains]

        numQs = 1

        #difficulties = ["difficulty = '" + d + "'" for d in difficulties]
        qStr = "SELECT * FROM clues WHERE (" + " OR ".join(["category = ?" for c in categories]) + ") AND (" + " OR ".join(["LOWER(question) LIKE ?" for q in qContains]) + ") AND (" + " OR ".join(["LOWER(answers) LIKE ?" for a in aContains]) + ") ORDER BY RANDOM() LIMIT ?"
        params = categories + qContains + aContains
        params.append(numQs)
        print(qStr)
        print(params)
        clue = queryDB(qStr, params)
        if len(clue) == 0:
            return json.dumps({"question": "None found", "answer": "None found"})

        clue = dict(clue[0])

        myDict = {"question": clue["question"], "answer": clue["answers"]}
        return json.dumps(myDict)
    else:
        return render_template('index.html')


@app.route("/write", methods = ["GET", "POST"])
def write():
    if request.method == "POST":
        question = request.form.get("question")
        answers = request.form.get("answers")
        category = request.form.get("category")
        
        qStr = "INSERT INTO clues (question, answers, category) VALUES (?, ?, ?)"
        queryDB(qStr, (question, answers, category))
        return json.dumps({"status": 200})

    else:
        return render_template('write.html')
