from models.models import *

def get_user_query(id = 1):
    user = User.get_by_id(id)
    return {
        "id": int(user.__str__()),
        "username": user.username,
        "group": user.group,
    }


def check_user_query(name):
    try:
        User.get(User.username == name)
    except:
        return False

    return True


def get_user_count_query():
    return User.select().count()

def get_user_list_query(offset=0, limit=15):
    userList = []

    for user in User.select().offset(offset).limit(limit):
        userList.append({
            "id": int(user.__str__()),
            "username": user.username,
            "group": user.group,
        })
    return userList

def create_user_query(jsonUser, username):
    cur_user = User.get(User.username == username)
    User(
        username = jsonUser["username"],
        password = jsonUser["password"],
        group = jsonUser["group"]
    ).save()

def update_user_query(id, jsonUser, username):
    cur_user = User.get(User.username == username)

    user = User().get_by_id(id)
    user.username = jsonUser["username"]
    if(jsonUser["password"] != ""):
        user.password = jsonUser["password"]
    user.group = jsonUser["group"]
    user.save()

def delete_user_query(id, username):
    cur_user = User.get(User.username == username)
    user = User().get_by_id(id)
    User().delete_by_id(id)

def get_group_query(username):
    user = User.get(User.username == username)
    return {
        "id" : user.get_id(),
        "username": user.username,
        "group": user.group
    }