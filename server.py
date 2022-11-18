from flask import Flask, render_template, request, flash, session, redirect
from model import db_connect, db
from forms import LoginForm
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "laguna"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
    
        user = customers.get_by_username(username)
        if not user or user ["password"] != password:
            flash("Invalid username or password")
            return redirect("/login")

        session["username"] = user['username']
        flash("Logged in.")
        return redirect("/melons")
    return render_template("login.html", form = form)


if __name__ == "__main__":
    db_connect(app)
    app.run(host="localhost", port = 5000, debug=True)