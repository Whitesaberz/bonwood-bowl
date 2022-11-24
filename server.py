from flask import Flask, render_template, request, flash, session, redirect
from model import db_connect, db
from form import LoginForm
import crud, time, random
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
    last_name = request.form.get("last_name")

    user = crud.get_user_by_email(email)
    if user:
        flash("User email already in use.")
    else:
        user = crud.create_user(email, password, last_name)
        db.session.add(user)
        db.session.commit()
        flash("User account created, please log in.")
        
        return redirect('/')
    
@app.route('/users/<user_id>')
def user_info(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user = user)

@app.route("/login", methods=["POST"])
def process_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:

        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")

@app.route("/logout")
def logout():
   del session["user_email"]
   flash("Logged out.")
   return redirect("/")

@app.route("/reservations", methods=["GET","POST"])
def create_reservation():

    logged_in_email = session.get("user_email")
    reservation_time = request.form.get("reservation")

    if logged_in_email is None:
        flash("You must log in to reserve a lane.")
    elif not reservation_time:
        flash("Error: you didn't select a time for your reservation.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        lane_options=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42"]
        lane = random.choice(int(lane_options))

        reservation = crud.create_reservation(user, lane, reservation_time)
        db.session.add(reservation)
        db.session.commit()

        flash(f"You reserved lane {lane} for {reservation_time}")

        return redirect("/cart")

if __name__ == "__main__":
    db_connect(app)
    app.run(host="localhost", port = 5000, debug=True)