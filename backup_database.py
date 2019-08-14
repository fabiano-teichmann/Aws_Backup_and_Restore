import os
from datetime import datetime
import subprocess
import zipfile
import shutil
from decouple import config
import boto3


class Backup(object):
    def __init__(self):
        self.path_base = config('path_backup')
        prefix = config('prefix_backup')
        strftime = config('format_date')
        now = datetime.now()
        now = now.strftime(strftime)
        backup = f"{prefix}_{now}"
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
        port = config('port')

        if db_auth and user and pwd:
            cmd = f"mongodump --host {url}:{port} -u {user} -p '{pwd}' --authenticationDatabase {db_auth}" \
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
        except Exception as e:
            raise e

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
            raise e

    def remove_folder(self):
        try:
            shutil.rmtree(self.folder)
            return True
        except:
            return False

    def upload_s3(self, zip_file):

        s3 = boto3.resource('s3')
        backup = os.path.split(zip_file)
        backup = backup[-1]
        resp_upload = s3.meta.client.upload_file(zip_file, self.bucket, backup)
        return resp_upload
