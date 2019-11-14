from models.models import *

def create_tables():
    User.create_table()
    Repository.create_table()
    Task.create_table()
    QueueTask.create_table()
