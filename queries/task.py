from models.models import *
import datetime

def get_task_query(id = 1):
    task = Task.get_by_id(id)
    print(task)
    return {
        "id": int(task.__str__()),

        "name": task.name,
        "mirror_url": task.mirror_url,
        "mirror_location": task.mirror_location,
        "mirror_type": task.mirror_type,
        "user": task.user.username,

        "schedule_status" : task.schedule_status,
        "schedule_run": task.schedule_run,
        "schedule_number": task.schedule_number,

        "schedule_minute" : task.schedule_minute,
        "schedule_hour" : task.schedule_hour,
        "schedule_day" : task.schedule_day,
        "schedule_month" : task.schedule_month,
        "schedule_year" : task.schedule_year,

        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }

def get_task_list_query(offset=0, limit=15):
    taskList = []

    for task in Task.select().offset(offset).limit(limit):
        taskList.append({
            "id": int(task.__str__()),
            "name": task.name,
            "user": task.user.username,
            "schedule_status": task.schedule_status,
            "schedule_run": task.schedule_run,
            "updated_at": task.updated_at
        })
    return taskList

def create_task_query(jsonTask, username):
    user = User.get(User.username == username)
    task = Task(
        name = jsonTask["name"],
        mirror_url=jsonTask["mirror_url"],
        mirror_location = jsonTask["mirror_location"],
        mirror_type=jsonTask["mirror_type"],
        user=user,

        schedule_status = jsonTask["schedule_status"],
        schedule_run=jsonTask["schedule_run"],
        schedule_number=jsonTask["schedule_number"],

        schedule_minute = jsonTask["schedule_minute"],
        schedule_hour = jsonTask["schedule_hour"],
        schedule_day = jsonTask["schedule_day"],
        schedule_month = jsonTask["schedule_month"],
        schedule_year = jsonTask["schedule_year"]
    ).save()

    Log(task = Task.get(Task.name == jsonTask["name"]), message="{} create".format(jsonTask["name"]), user=user).save()

def update_task_query(id, jsonTask, username):
    print(jsonTask)

    user = User.get(User.username == username)
    task = Task().get_by_id(id)

    task.name = jsonTask["name"]
    task.mirror_url = jsonTask["mirror_url"]
    task.mirror_location = jsonTask["mirror_location"]
    task.mirror_type = jsonTask["mirror_type"]

    task.schedule_status = jsonTask["schedule_status"]
    task.schedule_run = jsonTask["schedule_run"]
    task.schedule_number = jsonTask["schedule_number"]

    task.schedule_minute = jsonTask["schedule_minute"]
    task.schedule_hour = jsonTask["schedule_hour"]
    task.schedule_day = jsonTask["schedule_day"]
    task.schedule_month = jsonTask["schedule_month"]
    task.schedule_year = jsonTask["schedule_year"]

    task.updated_at = datetime.datetime.now()

    task.save()

    Log(task = task, message="{} update".format(jsonTask["name"]), user=user).save()

def delete_task_query(id, username):
    user = User.get(User.username == username)
    task = Task().get_by_id(id)
    Log(task = task, message="{} delete".format(task.name), user=user).save()
    Task().delete_by_id(id)

