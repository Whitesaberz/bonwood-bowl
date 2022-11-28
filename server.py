from flask import Flask, render_template, request, flash, session, redirect
from model import db_connect, db

import crud, datetime, random
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "laguna"
app.jinja_env.undefined = StrictUndefined

@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")

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
        flash("User email already in use.","error")
    else:
        user = crud.create_user(email, password, last_name)
        db.session.add(user)
        db.session.commit()
        flash("User account created, please log in.","success")
        
        return redirect('/')

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login/login_form", methods=["POST"])
def process_login():

    email = request.form.get("email")
    password = request.form.get("password")
    print(email)
    print(password)

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect. If you don't have an account, please create one.","error")
        return redirect("/login")
    else:

        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!", "success")

    return redirect("/")

@app.route("/logout")
def logout():
   del session["user_email"]
   flash("Logged out.", "success")
   return redirect("/")

@app.route("/reservations")
def reservations():

    logged_in_email = session.get("user_email")
    
    if logged_in_email is None:
        flash("You must log in to reserve a lane.", "error")
        return redirect("/login")
    else:
        return render_template("reservations.html")
    
@app.route("/reservations/create_reservation", methods=["GET", "POST"])
def create_reservation():
    
    logged_in_email = session.get("user_email")
    reservation_time = (request.form.get("reserve_time"))
    rental = request.form.get("rental")
    if rental:
        rental = True
    else:
        rental = False
    party_size = request.form.get("party_size")
    num_of_games = request.form.get("num_of_games")

    current_user = crud.get_user_by_email(logged_in_email)
    user = current_user.user_id
    lane_options=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42"]
    lane = int(random.choice(lane_options))

    reservation = crud.create_reservation(user, lane, reservation_time, rental, party_size, num_of_games)
    new_reservation = reservation.reservation_id
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    
    cart[new_reservation] = cart.get(new_reservation)
    session.modified = True
    flash(f"Reservation created for {reservation_time}, please commit in cart.", "success")
    print(new_reservation)
    return redirect("/cart")

@app.route("/cart")
def cart_page():
    return render_template("cart.html")

@app.route("/empty-cart")
def empty_cart():
    
    session["cart"] = {}
    flash("Reservation deleted.")

    return redirect("/cart")
    
if __name__ == "__main__":
    db_connect(app)
    app.run(host="localhost", port = 5000, debug=True)