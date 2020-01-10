from models.models import *

class RepositoryBase():
    def __init__(self, repo):
        self.repo = repo

    def get_started_message(self):
        return "task started"

    def get_finished_message(self):
        return "task finished"

    def log_write(self, msg):
        try:
            if type(msg) != str:
                msg = msg.decode('utf-8')
        except Exception as e:
            msg = "Unreadable characters!"
        if msg != "":
            Task(repository=self.repo.name, message=msg, user=User.get_by_id(1).username).save()

    def base(self):
        pass

    def run(self):
        self.log_write(self.get_started_message())
        code = self.base()
        self.log_write(self.get_finished_message())
        return code
