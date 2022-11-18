from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

   __tablename__ = "users"

   user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   email = db.Column(db.String, unique=True)
   password = db.Column(db.String)

   def __repr__(self):
      return f'<User user_id={self.user_id} email={self.email}>'

def db_connect(flask_app, db_uri="postgresql:///reservations",echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    db_connect(app)