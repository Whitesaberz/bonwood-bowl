"""CRUD Operations"""

from model import db, User, Lane, Reservation, Rental, db_connect

def create_user(email, password):

    user = User(email=email, password=password)

    return user

def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def create_lane(time, price_per_game):
    lane = Lane(
        time=time,
        price_per_game=price_per_game
    )
    return lane

def get_lanes():
    return Lane.query.all()

def get_lane_by_id(lane_id):
    return Lane.query.get(lane_id)

def create_reservation(user, lane, rental, time):
    reservation = Reservation(user=user, lane=lane, rental=rental, time=time)
    return reservation


def update_reservation(reservation_id, new_time):
    
    reservation = Reservation.query.get(reservation_id)
    reservation.time = new_time
    
def create_rental(shoe_size, price, reservation):
    rental = Rental(shoe_size, price, reservation)
    return rental
    

if __name__ == '__main__':
    from server import app
    db_connect(app)