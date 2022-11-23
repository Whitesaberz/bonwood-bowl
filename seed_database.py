import os
import json
from random import choice, randrange
from datetime import datetime, timedelta

import crud
import model
import server


os.system("dropdb reservations")
os.system("createdb reservations")

model.db_connect(server.app)
with server.app.app_context():
    model.db.create_all()

    with open("data/lanes.json") as lanes_json:
        lane_data = json.loads(lanes_json.read())
        
    lanes_in_db = []
    for lane in lane_data:
        price_per_game = (lane["price_per_game"])
        time = (lane["time"])

        db_lane = crud.create_lane(time, price_per_game)
        lanes_in_db.append(db_lane)

    model.db.session.add_all(lanes_in_db)
    model.db.session.commit()

    for n in range(10):
        email = f"user{n}@test.com"
        password = "test"

        user = crud.create_user(email, password)
        model.db.session.add(user)

        for _ in range(10):
            random_lane = choice(lanes_in_db)
            random_time = choice(lane.time)
            reservation = crud.create_reservation(user, random_lane, random_time)
            model.db.session.add(reservation)

    model.db.session.commit()