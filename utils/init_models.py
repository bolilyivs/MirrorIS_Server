from models.models import *

def init_user():
    User(username = "root", password = "123", group = 0).save()

def init_Task():
    Task(name = "debian",
         mirror_url="https://mirror.yandex.ru/debian/",
         mirror_location = "/home/mirrors/debian1",
         user = User.get_by_id(1)
         ).save()
    Log(message="debian mirror create", user = User.get_by_id(1)).save()

    Task(name="centos",
         mirror_url="https://mirror.yandex.ru/centos/",
         mirror_location="/home/mirrors/centos",
         user=User.get_by_id(1)
         ).save()
    Log(message="debian mirror create", user=User.get_by_id(1)).save()



