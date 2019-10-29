from models.models import *


def create_tables():
    Group.create_table()
    User.create_table()
    Task.create_table()
    Log.create_table()
