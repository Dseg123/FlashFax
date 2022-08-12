import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from sqlite3 import Error
import string
import random
import json
import pyttsx3
import time
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
    myConn = create_connection(r"/mnt/c/Users/aepst/Documents/Projects/Project2/proj2.db")
    myConn.row_factory = sqlite3.Row
    cur = myConn.cursor()
    cur.execute(query, vals)
    myConn.commit()
    answer = cur.fetchall()
    myConn.close()
    #print("inserted")
    return answer

def addQuestions(data):
    # with open(jsonFile, "r") as myFile:
    #     data = json.load(myFile)
    allTossups = data["data"]["tossups"]
    for myTossup in allTossups:
        myQuestion = myTossup["text"]
        myFormatQuestion = myTossup["formatted_text"]

        myAnswer = myTossup["answer"]
        myFormatAnswer = myTossup["formatted_answer"]

        myDifficulty = ""
        myCategory = ""
        mySubcategory = ""
        myTournament = ""
        if "name" in myTossup["tournament"]:
            myTournament = myTossup["tournament"]["name"]
        if "difficulty" in myTossup["tournament"]:
            myDifficulty = myTossup["tournament"]["difficulty"]
        if "name" in myTossup["category"]:
            myCategory = myTossup["category"]["name"]
        if "name" in myTossup["subcategory"]:
            mySubcategory = myTossup["subcategory"]["name"]

        queryDB("INSERT INTO tossups (body, formatBody, answer, formatAnswer, tournament, difficulty, category, subcategory) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (myQuestion, myFormatQuestion, myAnswer, myFormatAnswer, myTournament, myDifficulty, myCategory, mySubcategory))

# importing the requests library
import requests


categories = [26, 21, 20, 18, 15, 14, 25, 19, 17, 22, 16]
difficulties = ["middle_school", "easy_high_school", "regular_high_school", "hard_high_school", "national_high_school", "easy_college", "regular_college", "hard_college", "open"]


for category in categories:
    category = str(category) 
    for difficulty in difficulties:
        URL = "https://www.quizdb.org/api/search?search%5Bquery%5D=&search%5Bfilters%5D%5Bcategory%5D%5B%5D=" + category + "&search%5Bfilters%5D%5Bquestion_type%5D%5B%5D=Tossup&search%5Bfilters%5D%5Bdifficulty%5D%5B%5D=" + difficulty + "&search%5Blimit%5D=false"
        r = requests.get(url = URL)
        print(r.json()["data"]["num_tossups_shown"])
        addQuestions(r.json())


# addingQs = False
# gettingQs = False
# print(queryDB("SELECT * FROM tossups", ()))
# #def addQuestions(textFile, database):
    

# # while True:
# #     if addingQs:
# #         question = input("Enter your question:\n")
# #         if question == "quit":
# #             addingQs = False
# #             continue
# #         answer = input("Enter the answer to the question:\n")
# #         queryDB("INSERT INTO tossups (body, answer) VALUES (?, ?)", (question, answer))
# #         print("--------------------------------------")
# #     elif gettingQs:
# #         correct = 0
# #         total = 0
# #         myQs = queryDB("SELECT * FROM tossups ORDER BY RANDOM()")
# #         done = False
# #         for q in myQs:
# #             q = dict(q)
# #             ques = q["body"]
# #             ans = q["answer"]
# #             print("Question: " + ques)
# #             input("Your answer: ")
# #             print("Answer: " + ans)
# #             gotIt = input("Enter y if you got it or n if not: ")
# #             if gotIt.lower() == "y":
# #                 correct += 1
# #             total += 1
# #             cont = input("Enter y for continue: ")
# #             if cont.lower() != "y":
# #                 done = True
# #                 break
# #             print("----------------------------------------")
# #         if done:
# #             print("Portion correct: " + str(correct) + "/" + str(total))
# #             gettingQs = False
# #     else:
# #         try:
# #             resp = int(input("Type 1 for add question or 2 for get question: "))
# #             if resp == 1:
# #                 addingQs = True
# #             else:
# #                 gettingQs = True
# #         except:

# #             break