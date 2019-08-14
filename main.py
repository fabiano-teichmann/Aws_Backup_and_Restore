import time

import schedule
from decouple import config

from backup_database import Backup


def backup():
    backup = Backup()
    backup.backup()
    minutes = config('backup_interval', default=240)
    schedule.every(minutes).minutes.do(backup.backup)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    backup()

