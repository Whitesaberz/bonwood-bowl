import os
import json
from datetime import datetime

import crud
import model
import server

os.system("dropdb")
os.system("createdb")

model.db_connect(server.app)
model.db.create_all()