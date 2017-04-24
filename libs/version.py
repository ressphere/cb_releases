import glob
import re
import os
import pprint

class Version:
    def __init__(self, src):
        self.src_path = src
        self.file_version = []

    def update_version(self):
        pattern = r"\$config\['version'\].*"
        for fname in self.get_config_file():
            if os.path.isfile(fname) and 'config.php' in fname:
                with open(fname) as f:
                    try:
                        contents = f.readlines()
                        line = 0
                        for content in contents:
                            m = re.match(pattern, content)
                            if m:
                                splitted_content = content.split('=')
                                if(len(splitted_content) == 2):
                                    fname_version = (fname, line, splitted_content[1].strip(" ;\n"), int(splitted_content[1].strip(" ;\n")) + 1)
                                    self.file_version.append(fname_version)
                            line = line + 1
                    except:
                        pass
        self.write_version()

    def write_version(self):
        for (fname, line, old, new) in self.file_version:
            with open(fname, 'r+') as f:
                contents = f.readlines()
                contents[line] = contents[line].replace(old, str(new))
                f.writelines(contents)

    def get_config_file(self):
        #search_pattern = os.path.join(self.src_path)
        for path, subdirs, files in os.walk(self.src_path):
            for name in files:
                yield os.path.join(path, name)

