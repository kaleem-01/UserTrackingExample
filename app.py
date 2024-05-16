"""
Author: Kaleem Ullah (k.ullah2@uva.nl)

This program serves as a simple example of coding trackers using Flask. There are two variables tracked with this code:
(1) time spent on a specified page, (2) whether a specified button clicked or not.
"""

# If the below packages are not properly installed on your device, you will see a 'ModuleNotFoundError'.
# Then, you need to install the required packages using 'pip install' command in your terminal.
from flask import Flask, request, session, render_template, redirect
from datetime import datetime
from flask_session import Session
import sqlite3
from random import randint

#######################################
# The code used here is the standard for app configuration. The application is called "app" and it is a Flask object.
# The session is configured such that the files are stored in memory in the filesystem.
# The folder 'flask_session' is automatically generated once the application is executed and contains the data from user sessions.
# Using sqlite3, we connect to an existing database.


# Configure app using Flask
app = Flask(__name__)

# Connect to the database - before running this code, database file needs to be created using the create_table.sql code
# Our example database is already created and named as "test.db"
conn = sqlite3.connect("test.db", check_same_thread=False)
cur = conn.cursor()

# Configure flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session class sets up flask sessions for each new visitor
Session(app)
#######################################

#######################################
# This is the first user tracking function to log time spent on the previous page into the database. Unit of time is seconds.
# We calculate time spent by taking the difference of the timestamps taken now and when the user opens the page.
# The data is inserted into the `PageView` table in the 'test.db' database.


def log_data():
    if not all([key in session for key in ("id", "start_time", "previous_path")]):
        return

    session_id = session.get(
        "id"
    )  # Every session has an id. "id" variable is created later in the code. "session" variable holds the session specific information in Flask.
    start_time = session.get("start_time")
    previous_path = session.get("previous_path")

    # datetime class is used to access date and time
    time_spent = (datetime.now() - start_time).total_seconds()
    # Record is added to the database using sqlite
    cur.execute(
        "INSERT INTO PageView (session_id, page, time_spent, start_time) VALUES (?, ?, ?, ?)",
        (session_id, previous_path, time_spent, start_time),
    )
    conn.commit()


##################################################################################

##################################################################################
# After Each Request:


# 'after_request' decorator of Flask defines actions to be performed after each request coming from the client-side

# The function decorator `@app.after_request` is used with the `track_time()` function.
# This decorator runs the function after every request made by the user. A request here means requesting a webpage.
# This function basically runs at each webpage.
# The global variable `start_time` is used to keep track of time.
# The global variable `previous_path` is used to keep track of what the user visited before requesting the current page.
# `request.path` contains the information of the path of the website that the user requested.


@app.after_request
def track_time(response):
    # Every time the user requests default route (/), time spent in the previous path is recorded in the database with log_data().
    if request.path == "/":
        log_data()
        # Update start_time and previous_path
        session["start_time"] = datetime.now()
        session["previous_path"] = "HomePage"

    # Every time the user requests /learn_more route, time spent in the previous path is recorded in the database with log_data().
    if request.path == "/learn_more":
        log_data()
        # Update start_time and previous_path
        session["start_time"] = datetime.now()
        session["previous_path"] = "LearnMore"

    # Every time the user requests  /confirmation route, time spent in the previous path is recorded in the database with log_data().
    if request.path == "/confirmation":
        log_data()
        del session["start_time"]
        del session["previous_path"]

    return response


@app.before_request
def assign_id():
    # Every time a user accesses the website, a random ID is created because we need to track the user.
    # Information in each new user session can be stored as a 'key, value' pair in the `session` object.
    # Add id to the session
    if "id" not in session:
        session["id"] = randint(1_000_000, 9_999_999)


##################################################################################

##################################################################################
# Routes:

# Routing each webpage in the website can be done with the help of the `app.route()` decorator.
# The string inside this decorator can be considered as the name of the webpage. '/' refers to the index of the website. This is the homepage.
# The function runs when the specified route is requested by the user.
# For example, if the user opens the homepage, the `app.route('/')` is run, which allows the function `index()` to be executed and the html file ('index.html') is returned using the function `render_template`.


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/learn_more")
def learn_more():
    return render_template("learn_more.html")


@app.route("/confirmation")
def confirmation():
    return render_template("done.html")


# /log_binary is the route of this example website that users are sent to when they click on the "Contact" button (see 'index.html').
# However, it is a dummy route which does not render a new template. It redirects users to the Homepage.
# "Contact" button is added to provide an example structure for a button-click data collection.


@app.route("/log_binary")
# button_tracking() function saves the id to the 'Button' table of the database if the visitor clicked on the "Contact" button.
def button_tracking():
    if "id" not in session:
        return

    session_id = session.get("id")
    cur.execute(
        "INSERT INTO Button (session_id, button) VALUES (?, ?)", (session_id, 1)
    )
    conn.commit()

    return redirect("/")


##################################################################################

if __name__ == "__main__":
    app.run(port=3000, debug=True)
