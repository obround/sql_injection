from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "REDACTED"
app.config["SESSION_PERMANENT"] = False

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="REDACTED",
    password="REDACTED",
    hostname="REDACTED",
    databasename="REDACTED",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
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
        dict(name=res[0], age=res[1], email=res[2], years_employed=res[3])
        for res in results
    ]


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    employees = db_to_dict(db.engine.execute("SELECT * FROM employees"))
    if request.method == "POST":
        if "logout_button" in request.form:
            session.pop("logged_in", None)
            return redirect(url_for("login"))
        elif "search_button" in request.form:
            search_request = request.form["search_text"]
            return render_template(
                "dashboard.html",
                employees=db_to_dict(db.engine.execute(
                    f"SELECT * FROM employees WHERE name LIKE '%{search_request}%'"
                ))
            )
    return render_template("dashboard.html", employees=employees)


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = db.engine.execute(
            f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        )
        if len(list(result)) == 1:
            session.permanent = False
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Username or password is incorrect"
    return render_template("index.html", error=error)


if __name__ == "__main__":
    app.run()
