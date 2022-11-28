"""CRUD Operations"""

from model import db, User, Lane, Reservation, db_connect

def create_user(email, password, last_name):

    user = User(email=email, password=password, last_name=last_name)

    return user

def get_user_by_id(user_id):
    return User.query.filter(User.user_id == user_id).first()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def create_lane(price_per_game):
    return Lane(price_per_game=price_per_game)

def get_reservations():
    return Reservation.query.all()

def get_reservation_by_id(reservation_id):
    return Reservation.query.get(reservation_id)

def create_reservation(user_id, lane_id: int, time, rental_choice, party, num_of_games):
    return Reservation(user_id=user_id, lane_id=lane_id, time=time, rental_choice=rental_choice, party=party, num_of_games=num_of_games)

def update_reservation(reservation_id, new_time):
    
    reservation = Reservation.query.get(reservation_id)
    reservation.time = new_time   

if __name__ == '__main__':
    from server import app
    db_connect(app)