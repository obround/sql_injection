from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__)
app.secret_key = "because-you-know-this-so-u-can-perform-another-exploit"
app.config["SESSION_PERMANENT"] = False

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            return "You need to login first"

    return wrap


def db_to_dict(results):
    return [
        dict(id=res[0], name=res[1], age=res[2], email=res[3], years_employed=res[4])
        for res in results
    ]


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    with db.engine.connect() as conn:
        employees = db_to_dict(conn.execute(text("SELECT * FROM employees")))
        if request.method == "POST":
            if "logout_button" in request.form:
                session.pop("logged_in", None)
                return redirect(url_for("login"))
            elif "search_button" in request.form:
                search_request = request.form["search_text"]
                return render_template(
                    "dashboard.html",
                    employees=db_to_dict(conn.execute(text(
                        f"SELECT * FROM employees WHERE name LIKE '%{search_request}%'"
                    )))
                )
        return render_template("dashboard.html", employees=employees)


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with db.engine.connect() as conn:
            result = conn.execute(text(
                f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
            ))
        if len(list(result)) == 1:
            session.permanent = False
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Username or password is incorrect"
    return render_template("index.html", error=error)


if __name__ == "__main__":
    app.run()
