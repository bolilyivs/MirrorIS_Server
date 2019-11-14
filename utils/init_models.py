from models.models import *
from queries.repository import *

def init_user():
    User(username = "root", password = "123", group = 0).save()

def init_Task():
    create_repository_query({
  "mirror_location": "debian",
  "mirror_type": 0,
  "mirror_url": "rsync://mirror.yandex.ru/debian/doc/FAQ/",
  "name": "debian",
  "schedule_day": 0,
  "schedule_hour": 0,
  "schedule_minute": 1,
  "schedule_month": 0,
  "schedule_number": 2,
  "schedule_status": True,
  "schedule_year": 0
  }, "root")

    create_repository_query({
  "mirror_location": "centos",
  "mirror_type": 0,
  "mirror_url": "rsync://mirror.yandex.ru/debian/doc/FAQ/",
  "name": "centOS",
  "schedule_day": 0,
  "schedule_hour": 0,
  "schedule_minute": 1,
  "schedule_month": 0,
  "schedule_number": 2,
  "schedule_status": True,
  "schedule_year": 0
  }, "root")

    create_repository_query({
  "mirror_location": "opensuse",
  "mirror_type": 0,
  "mirror_url": "rsync://mirror.yandex.ru/debian/doc/FAQ/",
  "name": "opensuse",
  "schedule_day": 0,
  "schedule_hour": 0,
  "schedule_minute": 1,
  "schedule_month": 0,
  "schedule_number": 2,
  "schedule_status": False,
  "schedule_year": 0
  }, "root")

    create_repository_query({
        "mirror_location": "ubuntu",
        "mirror_type": 0,
        "mirror_url": "rsync://mirror.yandex.ru/debian/doc/FAQ/",
        "name": "ubuntu",
        "schedule_day": 0,
        "schedule_hour": 0,
        "schedule_minute": 2,
        "schedule_month": 0,
        "schedule_number": 2,
        "schedule_status": True,
        "schedule_year": 0
    }, "root")



