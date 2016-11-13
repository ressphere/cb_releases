__author__ = 'user'
from ftplib import FTP
import os
import pprint
import warnings
import logging
import threading


class ftp:
    def __init__(self, host, username="", password=""):
        self.host = host
        self.username = username
        self.password = password
        self.filters = []

    def set_filters(self, filter_list):
        self.filters += filter_list

    def create_file(self, source, dest):
        with open(source, 'rb') as f:
            if not self.disable_log:
                print("OPEN %s"%(source))
            self.ftp.storbinary('STOR %s'%dest, f)
            if not self.disable_log:
                print("STORED %s ==> %s"%(source,dest))

    # Check if directory exists (in current location)
    def directory_exists(self, targeted_folder_name):
        filelist = []
        self.ftp.retrlines('LIST',filelist.append)
        for f in filelist:
            if f.split()[-1] == targeted_folder_name and f.upper().startswith('D'):
                return True
        return False

    def create_folder(self, targeted_folder_name):
        dirs = targeted_folder_name.split('/')
        for dir_name in dirs:
            if not self.directory_exists(dir_name):
                if not self.disable_log:
                    print("CREATE %s"%dir_name)
                self.ftp.mkd(dir_name)
                break
            else:
                self.ftp.cwd(dir_name)
        self.ftp.cwd(self.ftp_root)


    def begin_upload(self, root, filename):
        filtered = False;
        releases_file = os.path.join(root, filename)

        for _filter in self.filters:
            if _filter in root:
                if not self.disable_log:
                    warnings.warn("IGNORE %s"%releases_file)
                filtered = True
                break
        if not filtered:
            ftp_file_path = releases_file.replace("%s%s"%(self.cwd, os.path.sep), self.ftp_root)
            ftp_file_path = ftp_file_path.replace(os.path.sep,'/')
            ftp_dir_path = os.path.dirname(ftp_file_path)
            print(ftp_dir_path)
            if ftp_dir_path != self.ftp_root:
                self.create_folder(ftp_dir_path.replace(self.ftp_root, "",1))
            self.create_file(source=releases_file, dest=ftp_file_path)

    def upload(self, root, filename, cwd, disable_log = False):
        self.disable_log = disable_log
        self.ftp_root = self.ftp.pwd()
        self.cwd = cwd
        self.begin_upload(root,filename)


    def __enter__(self):
        logging.info("ftp created on entering")
        self.ftp = FTP(self.host, self.username, self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info("ftp closing on exit")
        self.ftp.close()
