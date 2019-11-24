from tasks.TaskRunner import TaskRunner
from models.models import *

class ScheduleTaskRunner(TaskRunner):
    def run(self, task_id):
        self.change_status_run_on()
        thread = self.body()
        QueueTask.delete_by_id(task_id)
        self.set_status_run_off()
        return thread
