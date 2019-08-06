import os
from datetime import datetime
import subprocess
import zipfile
import shutil
from decouple import config


class Backup(object):
    def __init__(self):
        self.path_base = config('path_backup')
        self.prefix = config('prefix_bkp', default='backup')
        self.now = datetime.now()
        backup = f"{self.prefix}_{self.now.day}-{self.now.month}-{self.now.year}_" \
                 f"{self.now.hour}-{self.now.minute}"
        self.folder = os.path.join(self.path_base, backup)
        self.bucket = config('bucket_storage')

    def backup(self):
        dump = self.dump()
        if dump:
            zip_file = self.zip_folder()
            if zip_file:
                self.remove_folder()
                self.upload_s3(zip_file)

    def dump(self):

        url = config('url_database', default='localhost')
        user = config('user_database', default=False)
        pwd = config('pwd_database', default=False)
        db_auth = config('db_auth', default=False)

        if db_auth and user and pwd:
            cmd = f"mongodump --host {url}:27017 -u {user} -p '{pwd}' --authenticationDatabase {db_auth}" \
                  f" -o {self.folder}"
        else:
            cmd = f"mongodump -o {self.folder}"
        print(cmd)
        try:
            os.mkdir(self.folder)
            subprocess.call(cmd, shell=True)

            return True

        except FileExistsError:
           raise FileExistsError

    def zip_folder(self):
        try:
            path = os.path.join(self.path_base, self.folder)
            zip_file = f'{path}.zip'
            zip_ = zipfile.ZipFile(zip_file, 'w')
            for folder, subfolders, files in os.walk(path):
                for file in files:
                    zip_.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), path),
                               compress_type=zipfile.ZIP_DEFLATED)

            zip_.close()
            return zip_file

        except Exception as e:
           return False

    def remove_folder(self):
        try:
            shutil.rmtree(self.folder)
            return True
        except:
            return False

    def upload_s3(self, zip_file):

        cmd = f'aws s3 cp {zip_file} s3://{self.bucket}'
        try:
            cod = subprocess.call(cmd, shell=True)

            if cod == 0:
                os.remove(zip_file)
            return True
        except:

            return False
