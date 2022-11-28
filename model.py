from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

   __tablename__ = "users"

   user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   email = db.Column(db.String, unique=True)
   password = db.Column(db.String)
   last_name = db.Column(db.String)
   
   def __init__(self, email, password, last_name):
       self.email = email
       self.password = password
       self.last_name = last_name

   def __repr__(self):
       return f"{self.user_id}"
   

class Lane(db.Model):

    __tablename__ = "lanes"

    lane_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    price_per_game = db.Column(db.Float)
    
    def __init__(self, price_per_game):
        self.price_per_game = price_per_game
    
    def __repr__(self):
        return f"<Lane lane_id={self.lane_id} price_per_game={self.price_per_game}>"

class Reservation(db.Model):

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    lane_id = db.Column(db.Integer, db.ForeignKey("lanes.lane_id"))
    time = db.Column(db.DateTime)
    rental_choice = db.Column(db.Boolean)
    party = db.Column(db.Integer)
    num_of_games=db.Column(db.Integer)

    lane = db.relationship("Lane", backref="lanes")
    user = db.relationship("User", backref="users")
    
    def __init__(self, user_id, lane_id, time, rental_choice, party, num_of_games):
        self.user_id = user_id
        self.lane_id = lane_id
        self.time = time
        self.rental_choice = rental_choice
        self.party = party
        self.num_of_games = num_of_games
        
    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id} lane_id={self.lane_id} time={self.time} rental_choice={self.rental_choice} party={self.party} num_of_games={self.num_of_games} >"


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