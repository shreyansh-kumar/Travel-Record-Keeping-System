import functools
import random

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from travel_sys.db import get_db

pos_id_dict = {
    "hr" : 1,
    "emp" : 2,
    "acc" : 3
}

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        db.execute("SELECT * FROM login WHERE id = %s", (user_id,))
        g.user = (
            db.fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        id = random.randint(1,300)
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        password = request.form["password"]
        position = request.form["position"]
        dob = request.form["dob"]
        start_date = request.form["start_date"]
        email = request.form["email"]
        ssn = request.form["ssn"]
        acc_num = request.form["acc_num"]
        route_num = request.form["route_num"]
        db = get_db()
        error = None

        if not first_name:
            error = "First Name is required."
        elif not last_name:
            error = "Last Name is required."
        elif not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not position:
            error = "Position is required."
        elif not dob:
            error = "Date of Birth is required."
        elif not start_date:
            error = "Start Date is required."
        elif not email:
            error = "Email is required."
        elif not ssn:
            error = "SSN is required."
        elif not acc_num:
            error = "Account Number is required."
        elif not route_num:
            error = "Route Number is required."

        position_id = pos_id_dict[position]


        if error is None:
            #try:
                db.execute(
                    "INSERT INTO login (id, username, password, position_id) VALUES (%s, %s, %s, %s)",
                    (id, username, generate_password_hash(password), position_id)
                )
                db.execute("COMMIT")

                #id = db.execute(" SELECT id FROM login WHERE username = %s", (username,))

                db.execute (
                    " INSERT INTO employee (id, first_name, last_name, position, dob, start_date, email, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (id, first_name, last_name, position, dob, start_date, email, ssn)
                )
                db.execute("COMMIT")

                db.execute (
                    " INSERT INTO payment_info (id, acc_num, route_num) VALUES (%s, %s, %s)",
                    (id, acc_num, route_num)
                )
                db.execute("COMMIT")
            #except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                #error = "Username or Email or SSN is already registered."
            #else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        db.execute((
            "SELECT * FROM login WHERE username = %s"), 
            (username, )
        )
        employee = db.fetchone()

        if employee is None:
            error = "Incorrect username."
        elif not check_password_hash(employee[2], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = employee[0]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
