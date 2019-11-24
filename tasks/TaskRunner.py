from models.models import *
import sys
import trace
import threading
import time


class Thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def func():
    while True:
        print('thread running')

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
        thread = Thread_with_trace(
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


