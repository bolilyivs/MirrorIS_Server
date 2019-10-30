from models.models import *


def create_tables():
    User.create_table()
    Task.create_table()
    Log.create_table()
