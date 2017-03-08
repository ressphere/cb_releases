__author__ = 'VCFR67'


from libs.async_base import *
import datetime
import os
from libs.filelock import *
import glob
import shutil
from os import walk
import pprint

class FtpManager:
    pass

class StringParser(AsyncCall):
    def __init__(self):
        super(StringParser,self).__init__()

    @async
    ##
    ## replacements is a hash collection that key is the target, source is the replacement
    ## {"a;"b", "c":"d"}
    ##
    def begin_replacement(self, infile, replacements, outfile):

        print("reading %s"%(infile))
        input_file = open(infile)
        lines = input_file.readlines()
        for index in range(len(lines)):
            for src, target in replacements.items():
                lines[index] = lines[index].replace(src, target)
        input_file.close()

        print("writing %s"%(outfile))
        output_file = open(outfile, 'w')
        for line in lines:
            output_file.write(line)
        output_file.close()

    def execute(self, release_folder, file_need_to_parse):
        for parser in file_need_to_parse:
            for file in parser["files"]:
                full_file_name = os.path.join(release_folder, file.replace('/',os.path.sep).strip(os.path.sep))
                self.begin_replacement(full_file_name, parser["keys"], full_file_name)



class DirectoryFileManager(AsyncCall):
    def __init__(self, dev_source, release_folder = None):
        self.dev_source = dev_source
        self._release_folder = release_folder
        super(DirectoryFileManager,self).__init__()

    def begin_replacement(self, dev_source, replacement_source, release_folder = None):
        if release_folder is not None:
            self._release_folder = release_folder
        if(self.release_folder is None):
            raise Exception("release folder cannot be none")

    def copy_dev_dir_to_release_dir(self, dev_folder, dir_structure_list, release_folder = None):
        ## copy and move the directory base on setting
        if release_folder is None:
            release_folder = self.release_folder
        assert(release_folder)

        for dir_structure in dir_structure_list:
            print(dir_structure)
            for (target_folder, dest_folder) in dir_structure.items():
                target_folder = target_folder.replace("/", os.path.sep)
                dest_folder = dest_folder.replace("/", os.path.sep)

                target_folder = target_folder.strip(os.path.sep)
                dest_folder = dest_folder.strip(os.path.sep)

                target_full_path = os.path.join(dev_folder, target_folder)
                dest_folder_full_path = os.path.join(release_folder, dest_folder)
                if os.path.exists(target_full_path.strip('*')):
                    for target_file_folder in glob.glob(target_full_path):
                         if os.path.isdir(target_file_folder):
                            dirname = os.path.basename(target_file_folder)
                            dest_dirname = os.path.join(dest_folder_full_path, dirname)
                            shutil.copytree(target_file_folder, dest_dirname)
                         else:
                            filename = os.path.basename(target_file_folder)
                            dest_filename = os.path.join(dest_folder_full_path, filename)
                            if(not os.path.exists(dest_folder_full_path)):
                                os.makedirs(dest_folder_full_path)
                            shutil.copy(target_file_folder, os.path.join(dest_filename))

    def create_release_folder(self, force = False):
        d = datetime.date.today()
        dir_name = '%02d%02d%02d'%(d.day, d.month, d.year)
        if self.release_folder:
           dir_name = os.path.join(self.release_folder , dir_name)
        else:
            dir_name = os.path.join(os.getcwd() , dir_name)


        if os.path.exists(dir_name):
            if force:
                shutil.rmtree(dir_name, ignore_errors=True)
            else:
                raise Exception("File exists at %s, please delete"%dir_name)
        os.mkdir(dir_name)
        self._release_folder = dir_name

    def copy_targeted_dir(self):
        target_dir = os.path.join(os.getcwd(), "ressphere")
        for (dirpath, dirnames, filenames) in walk(target_dir):
            for filename in filenames:
                source_path_name = os.path.join(dirpath, filename).replace('/', os.path.sep)
                targeted_path_name = os.path.join(dirpath.replace(target_dir, self.release_folder), filename).replace('/', os.path.sep)
                shutil.copy(source_path_name, targeted_path_name)

    @property
    def release_folder(self):
        return self._release_folder





