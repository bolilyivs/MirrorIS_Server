from tasks.ScheduleTaskRunner import *
from  repository import RepositoryClasses
import time
from models.models import *

threadings = 2
threadList = {}

def get_repos():
  repos = Repository.select().where(
    (Repository.schedule_status == True) &
    (Repository.schedule_next_update <= datetime.datetime.now())).order_by(Repository.schedule_next_update)
  if repos.count() > 0:
    for repo in repos:
      print(repo.name, repo.schedule_next_update)
      if repo.name in threadList and threadList[repo.name].is_alive():
        threadList[repo.name].kill()
        print("thread", repo.name, "stop")
      try:
        QueueTask(repository = repo).save()
      except:
        pass
    return True
  else:
    False

def run_task():
  tasks = QueueTask.select().limit(threadings)
  if tasks and tasks.count() > 0:
    for task in tasks:
      if not task.repository.schedule_run:
        threadList[task.repository.name] = ScheduleTaskRunner(RepositoryClasses.RepositoryUpdate(task.repository)).run(task.get_id())

def clear_tasks():
  QueueTask.truncate_table()
  repos = Repository.select().where(Repository.schedule_run == True)
  if repos.count() > 0:
    for repo in repos:
      repo.schedule_run = False
      repo.save()


def main():
  threadList = []
  clear_tasks()
  while True:
    print("get_repos")
    if get_repos():
      print("run_task")
      run_task()
    print("sleep")
    time.sleep(20)

main()