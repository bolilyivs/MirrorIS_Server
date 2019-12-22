from utils.init_models import *
from utils.create_models import *
import threading

create_tables()
init_user()
#init_Task()

while threading.activeCount() > 1:
  time.sleep(5)
