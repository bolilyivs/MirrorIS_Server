from models.models import *

def get_task_query(id = 1):
    task = Task.get_by_id(id)
    return {
        "id": int(task.__str__()),
        "repository" : task.repository.name,
        "message": task.message,
        "user": task.user.username,
        "date": task.date,
    }

def get_task_count_query():
    return Task.select().count()

def get_task_list_query(offset=0, limit=15):
    taskList = []

    for task in Task.select().offset(offset).limit(limit):
        taskList.append({
            "id": int(task.__str__()),
            "repository": task.repository.name,
            "message": task.message,
            "user": task.user.username,
            "date": task.date,
        })
    return taskList