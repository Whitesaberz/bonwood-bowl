import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system("dropdb reservations")
os.system("createdb reservations")

model.db_connect(server.app)
with server.app.app_context():
    model.db.create_all()
    for i in range(42):
       new_lane = crud.create_lane(5.00)
       model.db.session.add(new_lane)
    model.db.session.commit()
    
    
    with open("data/reservations.json") as reservations_json:
        reservation_data = json.loads(reservations_json.read())
        
    reservations_in_db = []
    for reservation in reservation_data:
        time = (reservation["time"])

        db_reservation = crud.create_reservation(time)
        reservations_in_db.append(db_reservation)

    model.db.session.add_all(reservations_in_db)
    model.db.session.commit()

    for n in range(10):

        email = f"user{n}@test.com"
        password = "test"
        last_name = "test"
        user = crud.create_user(email, password, last_name)
        model.db.session.add(user)
    
        for r in range(1):
            group = randint(1, 20)
            rental_choice = True
            random_lane = randint(1, 42)
            random_hour = randint(10, 22)
            new_date=datetime(2022, 11, 30, hour=random_hour)
            reservation = crud.create_reservation(user, random_lane, new_date, rental_choice, group)
        model.db.session.add(reservation)
    model.db.session.commit()

            
    for l in range(4, 14):
        random_shoe_size = randint(4, 14)
        random_res = randint(1, 10)
        new_rental = crud.create_rental(random_shoe_size, 3.00, random_res)
        model.db.session.add(new_rental)
    model.db.session.commit()
