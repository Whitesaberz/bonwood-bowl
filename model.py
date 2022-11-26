from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

   __tablename__ = "users"

   user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   email = db.Column(db.String, unique=True)
   password = db.Column(db.String)
   last_name = db.Column(db.String)
   
   def __repr__(self):
      return f'<User user_id={self.user_id} email={self.email}>'


class Lane(db.Model):

    __tablename__ = "lanes"

    lane_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    price_per_game = db.Column(db.Float)
    
    def __repr__(self):
        return f"<Lane lane_id={self.lane_id} price_per_game={self.price_per_game}>"

class Reservation(db.Model):

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lane_id = db.Column(db.Integer, db.ForeignKey("lanes.lane_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    time = db.Column(db.DateTime)
    rental = db.Column(db.Boolean, default=False)

    lane = db.relationship("Lane", backref="reservations")
    user = db.relationship("User", backref="reservations")
    rental = db.relationship("Rental", backref="reservations")
        
    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id} time={self.time}>"


class Rental(db.Model):
    
    __tablename__ = "rentals"
    
    rental_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    shoe_size = db.Column(db.Integer)
    price = db.Column(db.Float)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.reservation_id"))
    
    reservation = db.relationship("Reservation", backref="reservations", overlaps="rental,reservations")

    def __repr__(self):
        return f"<Rental rental_id={self.rental_id} shoe_size={self.shoe_size}"

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