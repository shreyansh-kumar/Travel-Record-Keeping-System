from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from travel_sys.auth import login_required
from travel_sys.db import get_db

bp = Blueprint("sub", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    
    db.execute((
        " SELECT em.id, mode, t.booking_id, ticket_num, date_dep, date_arr, travel_time, cost"
        " FROM employee em JOIN "
        " travel_info t JOIN expense_info ex ON em.id = t.id and ex.id = t.id and ex.booking_id = t.booking_id"
        " ORDER BY cost DESC")
    )
    posts = db.fetchall()
    return render_template("sub/index.html", posts=posts)


def get_post(id, booking_id, check_author=True):
    """Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    db = get_db()
    
    db.execute((
        " SELECT em.id, mode, t.booking_id, t.ticket_num, t.date_dep, t.date_arr, t.travel_time, cost"
        " FROM employee em JOIN travel_info t JOIN expense_info ex "
        " ON em.id = t.id and ex.id = t.id and ex.booking_id = t.booking_id"
        " WHERE em.id = %s and t.booking_id = %s"), 
        (id, booking_id))
    

    post = db.fetchone()
    if post is None:
        abort(404, f"Post id {booking_id} doesn't exist.")

    if check_author and post[0] != g.user[0]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        id = g.user[0]
        mode = request.form["mode"]
        booking_id = request.form["booking_id"]
        ticket_num = request.form["ticket_num"]
        date_dep = request.form["date_dep"]
        date_arr = request.form["date_arr"]
        travel_time = request.form["travel_time"]
        cost = request.form["cost"]
        error = None

        if not mode:
            error = "Mode is required."
        elif not booking_id:
            error = "Booking ID is required."
        elif not ticket_num:
            error = "Ticket Number is required."
        elif not date_dep:
            error = "Date of Departure is required."
        elif not date_arr:
            error = "Date of Arrival is required."
        elif not cost:
            error = "Cost is required."
        

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO travel_info (id, mode, booking_id, ticket_num, date_dep, date_arr, travel_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (g.user[0], mode, booking_id, ticket_num, date_dep, date_arr, travel_time),
            )
            db.execute("COMMIT")

            db.execute(
                "INSERT INTO expense_info (id, booking_id, cost, paid) VALUES (%s, %s, %s, %s)" , (id, booking_id, cost, 0)
            )
            db.execute("COMMIT")
            return redirect(url_for("sub.index"))

    return render_template("sub/create.html")


@bp.route("/<int:id>/<int:booking_id>/update", methods=("GET", "POST"))
@login_required
def update(id, booking_id):
    """Update a post if the current user is the author."""
    post = get_post(id, booking_id)

    if request.method == "POST":
        mode = request.form["mode"]
        ticket_num = request.form["ticket_num"]
        date_dep = request.form["date_dep"]
        date_arr = request.form["date_arr"]
        travel_time = request.form["travel_time"]
        cost = request.form["cost"]
        error = None

        if not mode:
            error = "Mode is required."
        elif not ticket_num:
            error = "Ticket Number is required."
        elif not date_dep:
            error = "Date of Departure is required."
        elif not date_arr:
            error = "Date of Arrival is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                ("UPDATE travel_info SET mode = %s, ticket_num = %s, date_dep = %s, date_arr = %s, travel_time = %s WHERE id = %s and booking_id = %s"), (mode, ticket_num, date_dep, date_arr, travel_time, id, booking_id)
            )
            db.execute("COMMIT")

            db.execute(
                ("UPDATE expense_info SET cost = %s WHERE id = %s and booking_id = %s"), (cost, id, booking_id)
            )
            db.execute("COMMIT")
            return redirect(url_for("sub.index"))

    return render_template("sub/update.html", post=post)


@bp.route("/<int:id>/<int:booking_id>/delete", methods=("POST",))
@login_required
def delete(id, booking_id):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id, booking_id)
    db = get_db()
    db.execute(("DELETE FROM travel_info WHERE id = %s, booking_id = %s"), (id,booking_id))
    db.execute("COMMIT")
    db.execute(("DELETE FROM expense_info WHERE id = %s, booking_id = %s"), (id,booking_id))
    db.execute("COMMIT")
    return redirect(url_for("sub.index"))


@bp.route("/generate")
@login_required
def generate():
    """Show all payments."""
    db = get_db()
    db.execute((
        " SELECT  acc_num, route_num, cost"
        " FROM expense_info e JOIN payment_info p ON e.id = p.id"
        " ORDER BY cost DESC")
    )
    
    posts = db.fetchall()
    return render_template("sub/generate.html", posts=posts)