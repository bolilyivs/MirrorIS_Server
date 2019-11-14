from models.models import *
from threading import Thread

class TaskRunner:
    def __init__(self, repositoryClass):
        self.repo = repositoryClass.repo
        self.repositoryClass = repositoryClass

    def change_status_run_on(self):
        self.repo.schedule_run = True
        self.repo.save()

    def set_status_run_off(self):
        self.repo.schedule_run = False
        self.repo.save()

    def body(self):
        thread = Thread(
            target=lambda: self.repositoryClass.run()
        )
        thread.start()
        thread.name = self.repo.name
        return thread

    def run(self):
        self.change_status_run_on()
        thread = self.body()
        self.set_status_run_off()
        return thread