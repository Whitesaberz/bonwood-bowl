from flask import Flask, render_template, request, flash, session, redirect
from model import db_connect, db
import crud, time
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "laguna"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("User email already in use.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("User account created, please log in.")
        
        return redirect('/')
    
@app.route('/users/<user_id>')
def user_info(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user = user)

@app.route('/login', methods=['POST'])
def retrieve_login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Signed in successfully, {user.email}!")

    return redirect("/")

@app.route("/lanes/<lane_id>/reservation", methods=["POST"])
def create_reservation(lane_id):

    logged_in_email = session.get("user_email")
    reservation_time = request.form.get("reservation")

    if logged_in_email is None:
        flash("You must log in to reserve a lane.")
    elif not reservation_time:
        flash("Error: you didn't select a time for your reservation.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        lane = crud.get_lane_by_id(lane_id)

        reservation = crud.create_reservation(user, lane, time.time(reservation_time))
        db.session.add(reservation)
        db.session.commit()

        flash(f"You reserved this lane {reservation_time}")

    return redirect(f"/cart")

if __name__ == "__main__":
    db_connect(app)
    app.run(host="localhost", port = 5000, debug=True)