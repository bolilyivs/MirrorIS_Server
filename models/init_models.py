from models.models import *
import hashlib

def init_groups():
    Group(name = "admin").save()
    Group(name = "user").save()

def init_user():
    User(username = "root", password = "123", group = Group.get(name="admin")).save()

def init_Task():
    Task(name = "debian",
         mirrorURL="https://mirror.yandex.ru/debian/",
         mirrorLocation = "/home/mirrors/debian1",
         user = User.get_by_id(1)
         ).save()
    Log(message="debian mirror create", user = User.get_by_id(1)).save()

    Task(name="centos",
         mirrorURL="https://mirror.yandex.ru/centos/",
         mirrorLocation="/home/mirrors/centos",
         user=User.get_by_id(1)
         ).save()
    Log(message="debian mirror create", user=User.get_by_id(1)).save()



