from repository.RepositoryBase import RepositoryBase
from repository.scripts import *
from dateutil.relativedelta import *
import time
import config

##############################################
class RepositoryCreate(RepositoryBase):

    def get_started_message(self):
        return "repository started create"

    def get_finished_message(self):
        return "repository finished create"

    def base(self):
        dir_path = f"{self.repo.mirror_zpool}/{self.repo.mirror_location}"
        code = create(dir_path)
        if(code != 0):
            self.log_write("Error create")
            return 1
        print("create", dir_path)

        return 0

##############################################
class RepositoryUpdate(RepositoryBase):

    def update_date_task(self):
        date = datetime.datetime.now()
        date += relativedelta(
            year=self.repo.schedule_year,
            month=self.repo.schedule_month,
            day=self.repo.schedule_day)
        date += datetime.timedelta(
            hours=self.repo.schedule_hour,
            minutes=self.repo.schedule_minute)
        self.repo.schedule_next_update = date
        self.repo.save()

    def get_started_message(self):
        return "repository started update"

    def get_finished_message(self):
        return "repository finished update"

    def get_error_message(self):
        return "repository error update"

    def get_snapshot_error_message(self):
        return "repository error snapshot"

    def base(self):
        self.update_date_task()
        dir_path = f"{self.repo.mirror_zpool}/{self.repo.mirror_location}"

        if(update(dir_path, self.repo.mirror_url, self.repo.mirror_args) != 0):
            self.log_write(self.get_error_message())
            return -1
        print("update", dir_path, self.repo.mirror_args)

        if(snapshot(dir_path, self.repo.schedule_number) != 0):
            self.log_write(self.get_snapshot_error_message())
            return -2

        print("snapshot", dir_path, self.repo.schedule_number)

        return 0


##############################################
class RepositoryDelete(RepositoryBase):
    def get_started_message(self):
        return "repository started delete"

    def get_finished_message(self):
        return "repository finished delete"

    def base(self):
        dir_path = f"{self.repo.mirror_zpool}/{self.repo.mirror_location}"
        delete(dir_path)
        print("delete", dir_path)
        return 0

##############################################
class RepositoryFullCreate(RepositoryBase):
    def get_started_message(self):
        return "repository started full create"

    def get_finished_message(self):
        return "repository finished full create"

    def base(self):
        if RepositoryCreate(self.repo).run() != 0:
            print("RepositoryCreate", "error")
            return -1
        if RepositoryUpdate(self.repo).run() != 0:
            print("RepositoryUpdate", "error")
            return -2
        print("full create")

##############################################
class RepositoryReset(RepositoryBase):
    def get_started_message(self):
        return "repository started reset"

    def get_finished_message(self):
        return "repository finished reset"

    def base(self):
        if RepositoryDelete(self.repo).run() != 0:
            print("RepositoryDelete", "error")
            return -1
        if RepositoryCreate(self.repo).run() != 0:
            print("RepositoryCreate", "error")
            return -2
        if RepositoryUpdate(self.repo).run() != 0:
            print("RepositoryUpdate", "error")
            return -3
        print("reset")

##############################################




