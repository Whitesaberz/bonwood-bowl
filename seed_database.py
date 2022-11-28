import os
from random import randint
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

    for n in range(10):
        email = f"user{n}@test.com"
        password = "test"
        last_name = "test"
        
        user = crud.create_user(email, password, last_name)
        model.db.session.add(user)
        model.db.session.commit()
    
        for r in range(1):
            game_count = randint(1, 7)
            group = randint(1, 20)
            rental_choice = True
            random_lane = randint(1, 43)
            random_hour = randint(10, 23)
            new_date=datetime(2022, 11, 30, hour=random_hour)
            
            reservation = crud.create_reservation(user.user_id, random_lane, new_date, rental_choice, group, game_count)
            model.db.session.add(reservation)
            model.db.session.commit()