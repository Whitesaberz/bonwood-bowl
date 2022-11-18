from flask import Flask, render_template, request, flash, session, redirect
from model import db_connect, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "laguna"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template("homepage.html")

if __name__ == "__main__":
    db_connect(app)
    app.run(host="localhost", port = 5000, debug=True)