from peewee import *
from models.db_getter import get_db
import datetime
import hashlib

db = get_db()

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField()
    password = CharField()
    group = IntegerField()

    def sha256(self, passwd):
        return hashlib.sha256(passwd.encode('utf-8')).hexdigest()


class Repository(BaseModel):
    name = CharField()
    mirror_url = CharField()
    mirror_zpool = CharField()
    mirror_location = CharField()
    mirror_type = IntegerField(default=0)
    mirror_args = CharField()
    mirror_init = BooleanField(default=False)

    user = ForeignKeyField(User, backref='tasks', on_delete='cascade')

    schedule_status = BooleanField(default=False)
    schedule_run = BooleanField(default=False)
    schedule_number = IntegerField(default=1)

    schedule_minute = IntegerField(default=0)
    schedule_hour = IntegerField(default=0)
    schedule_day = IntegerField(default=0)
    schedule_month = IntegerField(default=0)
    schedule_year = IntegerField(default=0)

    schedule_next_update = DateTimeField(default=datetime.datetime.now())

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

class Task(BaseModel):
    message = CharField()
    repository = CharField()
    user = CharField()
    date = DateTimeField(default=datetime.datetime.now)

class QueueTask(BaseModel):
    repository = ForeignKeyField(Repository, backref='repositories', unique=True, on_delete='cascade')