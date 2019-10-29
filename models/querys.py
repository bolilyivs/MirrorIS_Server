from models.models import *

def get_task_query(id = 1):
    task = Task.get_by_id(id)
    print(task)
    return {
        "id": int(task.__str__()),
        "name": task.name,
        "mirrorURL": task.mirrorURL,
        "mirrorLocation": task.mirrorLocation,
        "user": task.user.username,
        "updated_at": task.updated_at,

        "schedule_status" : task.schedule_status,
        "schedule_minute" : task.schedule_minute,
        "schedule_hour" : task.schedule_hour,
        "schedule_day" : task.schedule_day,
        "schedule_month" : task.schedule_month,
        "schedule_year" : task.schedule_year
    }

def get_task_list_query(offset=0, limit=15):
    taskList = []

    for task in Task.select().offset(offset).limit(limit):
        taskList.append({
            "id": int(task.__str__()),
            "name": task.name,
            "user": task.user.username,
            "schedule_status": task.schedule_status,
            "updated_at": task.updated_at
        })
    return taskList

def create_task_query(jsonTask, username):
    user = User.get(User.username == username)
    Task(
        name = jsonTask["name"],
        mirrorLocation = jsonTask["mirrorLocation"],
        mirrorURL = jsonTask["mirrorURL"],
        schedule_status = jsonTask["schedule_status"],
        schedule_minute = jsonTask["schedule_minute"],
        schedule_hour = jsonTask["schedule_hour"],
        schedule_day = jsonTask["schedule_day"],
        schedule_month = jsonTask["schedule_month"],
        schedule_year = jsonTask["schedule_year"],
        user = user
    ).save()

    Log(message="{} create".format(jsonTask["name"]), user=user).save()

def update_task_query(id, jsonTask, username):
    print(jsonTask)

    user = User.get(User.username == username)
    task = Task().get_by_id(id)

    task.name = jsonTask["name"]
    task.mirrorLocation = jsonTask["mirrorLocation"]
    task.mirrorURL = jsonTask["mirrorURL"]
    task.schedule_status = jsonTask["schedule_status"]
    task.schedule_minute = jsonTask["schedule_minute"]
    task.schedule_hour = jsonTask["schedule_hour"]
    task.schedule_day = jsonTask["schedule_day"]
    task.schedule_month = jsonTask["schedule_month"]
    task.schedule_year = jsonTask["schedule_year"]

    task.save()

    Log(message="{} update".format(jsonTask["name"]), user=user).save()

def delete_task_query(id, username):
    user = User.get(User.username == username)
    task = Task().get_by_id(id)
    Log(message="{} delete".format(task.name), user=user).save()
    Task().delete_by_id(id)

