__author__ = 'VCFR67'

import sys
import argparse

import libs
from minifier import *
from libs.ftp_connection import *
import threading
import ctypes  # An included library with Python install.


def start_upload(host, username, password, root, filenames, ftp_upload_filter_list, release_dir, disable_log, th_event):
    try:
        with libs.ftp(server, username, password) as FtpAgent:
            print("filter apply: ", ftp_upload_filter_list)
            FtpAgent.set_filters(ftp_upload_filter_list)
            for filename in filenames:
                FtpAgent.upload(root, filename, release_dir, disable_log)
    finally:
        th_event.set()

if __name__ == "__main__":
    MinifyAgent = None
    ftp_upload_filter_list = [
        os.path.join('properties', 'assets'),
        ".git",
        "db"
    ]
    # argument parser
    parser = argparse.ArgumentParser(description='Argument require for specify the path and action to release the script')
    parser.add_argument('--path',type=str, required=True,
                   help='path that contains the site files. eg: C:\\xampp\\htdocs\\cb_iloveproperty\\trunk')
    parser.add_argument('--minify', '-m', action='store_true', required=False,
                   help='add this argument if we want to minify the website size')
    parser.add_argument('--upload', nargs=3,
                   help='direct ftp upload, require 3 args: host username password')
    parser.add_argument('--disabled_logging', action='store_true',
                   help='disable print')

    args = parser.parse_args()

    if "htdocs" not in args.path or "trunk" not in args.path:
        sys.stderr.write("development directory with htdocs and trunk required")
        exit(-1)
    if args.minify:
        MinifyAgent = minifier()
    ver = libs.Version(args.path)
    ver.update_version()

    DirectoryManager = libs.DirectoryFileManager(args.path, os.getcwd())
    DirectoryManager.create_release_folder(True)
    DirectoryManager.copy_dev_dir_to_release_dir(args.path,settings.structure)
    DirectoryManager.copy_targeted_dir()
    StringParserManager = libs.StringParser()
    StringParserManager.execute(DirectoryManager.release_folder,settings.file_need_to_parse)
    if MinifyAgent:
        MinifyAgent.minify_string(DirectoryManager.release_folder)

    if args.upload and len(args.upload) == 3:
        (server, username, password) = args.upload
        disable_logging = args.disabled_logging
        counter = 0
        upload_event = threading.Event()

        for root, directories, filenames in os.walk(DirectoryManager.release_folder):
            required_args = (server,
                            username,password,
                            root,filenames,
                            ftp_upload_filter_list,
                            DirectoryManager.release_folder, args.disabled_logging, upload_event)

            th = threading.Thread(target=start_upload,args=required_args)
            upload_event.clear()
            th.start()

            counter = counter + 1
            if counter > 5:
                upload_event.wait()
                counter = counter -1
    ctypes.windll.user32.MessageBoxW(0, "js and css version updated, please checkin %s"%(args.path), "Updated version", 1)
    print(args.path)



