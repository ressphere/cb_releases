__author__ = 'VCFR67'
#main entry
import sys
import libs
import os
import settings
from minifier import *
from rcssmin import *
if __name__ == "__main__":

    MinifyAgent = None
    if len(sys.argv) < 2:
        sys.stderr.write("development directory contains the code is require")
    if "htdocs" not in sys.argv[1] and "trunk" not in sys.argv[1]:
        sys.stderr.write("development directory with htdocs and trunk required")
    if len(sys.argv) == 3 and sys.argv[2] == "minify":
        MinifyAgent = minifier()
    DirectoryManager = libs.DirectoryFileManager(sys.argv[1], os.getcwd())
    DirectoryManager.create_release_folder(True)
    DirectoryManager.copy_dev_dir_to_release_dir(sys.argv[1],settings.structure)
    DirectoryManager.copy_targeted_dir()
    StringParserManager = libs.StringParser()
    StringParserManager.execute(DirectoryManager.release_folder,settings.file_need_to_parse)
    if MinifyAgent:
        MinifyAgent.minify_string(DirectoryManager.release_folder)
    #begin_parsing(DirectoryManager.release_folder)



