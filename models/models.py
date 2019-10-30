from peewee import *
import config
import datetime


db = MySQLDatabase(
    database = config.db_name,
    user = config.db_user,
    password = config.db_password,
    host = config.db_host
)


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField()
    password = CharField()
    group = IntegerField()

class Log(BaseModel):
    message = CharField()
    user = ForeignKeyField(User, backref='logs')
    date = DateTimeField(default=datetime.datetime.now)

class Task(BaseModel):
    name = CharField()
    mirror_url = CharField()
    mirror_location = CharField()
    mirror_type = IntegerField(default=0)
    user = ForeignKeyField(User, backref='tasks')

    schedule_status = BooleanField(default=False)
    schedule_run = BooleanField(default=False)
    schedule_number = IntegerField(default=1)

    schedule_minute = IntegerField(default=0)
    schedule_hour = IntegerField(default=0)
    schedule_day = IntegerField(default=0)
    schedule_month = IntegerField(default=0)
    schedule_year = IntegerField(default=0)

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

