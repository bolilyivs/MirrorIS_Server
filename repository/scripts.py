# coding=utf-8
import datetime
import subprocess
import time
import config

# создает файловую систему zfs в dir_path
def create(dir_path):
    if not config.isWork:
        print(f"Task Create {dir_path}")
        return (0, "ok")
    else:
        try:
            return (0, subprocess.check_output(["zfs", "create", dir_path]))
        except subprocess.CalledProcessError as e:
            return (1, e.output)


# rsync выполняет синхронизацию с address_server в dir_path -> zstorage/test3
# v - увеличить уровень подробностей
# a - архивный режим
# H - сохранять жесткие ссылки
# z - сжимать поток передачи данных

def update(dir_path, address_server, args = "-vaHz"):
    if not config.isWork:
        print(f"Task update args = {args}")
        return (0, "ok")
    else:
        try:
            return (0, subprocess.check_output(["rsync", args, address_server, "/" + dir_path + "/"])[-20000:])
        except subprocess.CalledProcessError as e:
            return (1, e.output)


# create snapshot and delete last if count_snapshot >
def snapshot(dir_path, count_snapshot):
    if not config.isWork:
        print(f"Task snapshot count_snaps = {count_snapshot}; dir = {dir_path}")
        return (0, "ok")
    else:
        try:
            snapname = str(datetime.datetime.now())
            snapname = snapname.replace(' ', '_')
            res = subprocess.check_output(["zfs", "snapshot", dir_path + "@" + snapname])

            # берем количество существующих dir_path
            isMore = "zfs list -H -t snapshot -o name -S creation -r " + dir_path + " | wc -l"
            # subprocess.call(isMore, shell=True)

            # если их больше то удаляем
            if int(subprocess.check_output(isMore, shell=True)) > count_snapshot:
                delete = "zfs list -H -t snapshot -o name -S creation -r " + dir_path + " | tail -1 | xargs -n 1 zfs  destroy"
                res + subprocess.check_output(delete, shell=True)
            return (0, res)

        except subprocess.CalledProcessError as e:
            return (1, e.output)


def reset(dir_zfs):
    if not config.isWork:
        print("Task reset")
        return (0, "ok")
    else:
        # delete zfs file system
        delete(dir_zfs)
        # create zfs
        create(dir_zfs)
        return 0


def delete(dir_zfs):
    if not config.isWork:
        print(f"Task delete dir= {dir_zfs}")
        return (0, "ok")
    else:
        try:
            return (0, subprocess.check_output(["zfs", "destroy", "-r", dir_zfs]))
        except subprocess.CalledProcessError as e:
            return (1, e.output)

def get_zpool_list():
    if not config.isWork:
        return (0, "zroot")
    else:
        try:
            zpool_list = "zpool list | awk '{if (FNR > 1) print $1}'"
            return (0, subprocess.check_output(zpool_list, shell=True))
        except subprocess.CalledProcessError as e:
            return (1, e.output)