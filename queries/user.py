from models.models import *

def get_user_query(id = 1):
    user = User.get_by_id(id)
    return {
        "id": int(user.__str__()),

        "username": user.username,
        "group": user.group,
    }

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

    Log(message="{} create".format(jsonUser["username"]), user=cur_user).save()

def update_user_query(id, jsonUser, username):
    cur_user = User.get(User.username == username)

    user = User().get_by_id(id)
    user.username = jsonUser["username"]
    user.password = jsonUser["password"]
    user.group = jsonUser["group"]
    user.save()

    Log(message="{} update".format(jsonUser["username"]), user=cur_user).save()

def delete_user_query(id, username):
    cur_user = User.get(User.username == username)
    user = User().get_by_id(id)
    Log(message="{} delete".format(user.username), user=cur_user).save()
    User().delete_by_id(id)