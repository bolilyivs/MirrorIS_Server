from models.models import *

def get_log_query(id = 1):
    log = Log.get_by_id(id)
    return {
        "id": int(log.__str__()),
        "task" : log.task.name,
        "message": log.message,
        "user": log.user.username,
        "date": log.date,
    }

def get_log_list_query(offset=0, limit=15):
    logList = []

    for log in Log.select().offset(offset).limit(limit):
        logList.append({
            "id": int(log.__str__()),
            "task": log.task.name,
            "message": log.message,
            "user": log.user.username,
            "date": log.date,
        })
    return logList