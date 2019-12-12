from models.models import *
from queries.repository import *


def init_user():
    User(username="root", password=User().sha256("123"), group=0).save()
    User(username="user1", password=User().sha256("123"), group=1).save()


def init_Task():
    for i in range(2):
        create_repository_query({
            "mirror_zpool": "zroot",
            "mirror_args": "-vaHz",
            "mirror_location": f"debian{i}",
            "mirror_type": 0,
            "mirror_url": "rsync://mirror.yandex.ru/debian/doc/FAQ/",
            "name": f"debian{i}",
            "schedule_day": 0,
            "schedule_hour": 0,
            "schedule_minute": 1,
            "schedule_month": 0,
            "schedule_number": 2,
            "schedule_status": True,
            "schedule_year": 0
        }, "root")

        create_repository_query({
            "mirror_zpool": "zroot",
            "mirror_args": "-vaHz",
            "mirror_location": f"centos{i}",
            "mirror_type": 0,
            "mirror_url": "rsync://mirror.yandex.ru/debian/doc/FAQ/",
            "name": f"centOS{i}",
            "schedule_day": 0,
            "schedule_hour": 0,
            "schedule_minute": 1,
            "schedule_month": 0,
            "schedule_number": 2,
            "schedule_status": True,
            "schedule_year": 0
        }, "user1")

        create_repository_query({
            "mirror_zpool": "zroot",
            "mirror_args": "-vaHz",
            "mirror_location": f"opensuse{i}",
            "mirror_type": 0,
            "mirror_url": "rsync://mirror.yandex.ru/debian/doc/FAQ/",
            "name": f"opensuse{i}",
            "schedule_day": 0,
            "schedule_hour": 0,
            "schedule_minute": 1,
            "schedule_month": 0,
            "schedule_number": 2,
            "schedule_status": False,
            "schedule_year": 0
        }, "user1")

        create_repository_query({
            "mirror_location": f"ubuntu{i}",
            "mirror_zpool": "zroot",
            "mirror_args": "-vaHz",
            "mirror_type": 0,
            "mirror_url": "rsync://mirror.yandex.ru/debian/doc/FAQ/",
            "name": f"ubuntu{i}",
            "schedule_day": 0,
            "schedule_hour": 0,
            "schedule_minute": 2,
            "schedule_month": 0,
            "schedule_number": 2,
            "schedule_status": True,
            "schedule_year": 0
        }, "root")
