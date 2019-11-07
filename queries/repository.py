from models.models import *
import datetime

def get_repository_query(id = 1):
    repository = Repository.get_by_id(id)
    print(repository)
    return {
        "id": int(repository.__str__()),

        "name": repository.name,
        "mirror_url": repository.mirror_url,
        "mirror_location": repository.mirror_location,
        "mirror_type": repository.mirror_type,
        "user": repository.user.username,

        "schedule_status" : repository.schedule_status,
        "schedule_run": repository.schedule_run,
        "schedule_number": repository.schedule_number,

        "schedule_minute" : repository.schedule_minute,
        "schedule_hour" : repository.schedule_hour,
        "schedule_day" : repository.schedule_day,
        "schedule_month" : repository.schedule_month,
        "schedule_year" : repository.schedule_year,

        "created_at": repository.created_at,
        "updated_at": repository.updated_at,
    }

def get_repository_list_query(offset=0, limit=15):
    repositoryList = []

    for repository in Repository.select().offset(offset).limit(limit):
        repositoryList.append({
            "id": int(repository.__str__()),
            "name": repository.name,
            "user": repository.user.username,
            "schedule_status": repository.schedule_status,
            "schedule_run": repository.schedule_run,
            "updated_at": repository.updated_at
        })
    return repositoryList

def create_repository_query(jsonRepository, username):
    user = User.get(User.username == username)
    repository = Repository(
        name = jsonRepository["name"],
        mirror_url=jsonRepository["mirror_url"],
        mirror_location = jsonRepository["mirror_location"],
        mirror_type=jsonRepository["mirror_type"],
        user=user,

        schedule_status = jsonRepository["schedule_status"],
        schedule_run=jsonRepository["schedule_run"],
        schedule_number=jsonRepository["schedule_number"],

        schedule_minute = jsonRepository["schedule_minute"],
        schedule_hour = jsonRepository["schedule_hour"],
        schedule_day = jsonRepository["schedule_day"],
        schedule_month = jsonRepository["schedule_month"],
        schedule_year = jsonRepository["schedule_year"]
    ).save()

    Task(repository = Repository.get(Repository.name == jsonRepository["name"]), message="{} create".format(jsonRepository["name"]), user=user).save()

def update_repository_query(id, jsonRepository, username):
    print(jsonRepository)

    user = User.get(User.username == username)
    repository = Repository().get_by_id(id)

    repository.name = jsonRepository["name"]
    repository.mirror_url = jsonRepository["mirror_url"]
    repository.mirror_location = jsonRepository["mirror_location"]
    repository.mirror_type = jsonRepository["mirror_type"]

    repository.schedule_status = jsonRepository["schedule_status"]
    repository.schedule_run = jsonRepository["schedule_run"]
    repository.schedule_number = jsonRepository["schedule_number"]

    repository.schedule_minute = jsonRepository["schedule_minute"]
    repository.schedule_hour = jsonRepository["schedule_hour"]
    repository.schedule_day = jsonRepository["schedule_day"]
    repository.schedule_month = jsonRepository["schedule_month"]
    repository.schedule_year = jsonRepository["schedule_year"]

    repository.updated_at = datetime.datetime.now()

    repository.save()

    Task(repository = repository, message="{} update".format(jsonRepository["name"]), user=user).save()

def delete_repository_query(id, username):
    user = User.get(User.username == username)
    repository = Repository().get_by_id(id)
    Task(repository = repository, message="{} delete".format(repository.name), user=user).save()
    Repository().delete_by_id(id)

