import csv
from typing import Optional
from models import *

DATABASE_FILENAME = "fotografos.csv"
column_fields = ["id", "name", "condition"]

#show all photographers
def read_all():
    with open(DATABASE_FILENAME) as csvfile:
        reader = csv.DictReader(csvfile)
        return [PhotographerWithId(**row) for row in reader]

#show a photographer by the id
def read_one(photographer_id):
    with open(DATABASE_FILENAME) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["id"]) == photographer_id:
                return PhotographerWithId(**row)

