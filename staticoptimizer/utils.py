from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor
import logging
import os
import re
import subprocess

logger = logging.getLogger("labandas")

class FileOptimizer(object):
    root_path = settings.STATICFILES_DIRS[0] 
    
    def __init__(self):
        self.input_file_path = None
        self.output_file_path = None
        self.file_type = None
        self.apply_less = False
        
    def load(self, input_path):
        self.file_type = os.path.splitext(input_path)[1].lstrip(".")
        self.input_file_path = os.path.join(self.root_path, input_path)
        self.output_file_path = self.__get_output_file(input_path)
        return self
    
    def build(self):
        if os.path.exists(self.output_file_path) and not settings.DEBUG:
            return self.__get_file_name()
        
        self.__create_dirs()
            
        self.__build_file()
        
        self.__delete_old_files()
        
        return self.__get_file_name() 
    
    def with_less(self):
        self.apply_less = True
        return self
    

    def __create_dirs(self):
        output_directory = os.path.dirname(self.output_file_path)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    
    def __delete_old_files(self):
        output_directory = os.path.dirname(self.output_file_path)
        compiled_filename = os.path.split(self.output_file_path)[-1]
        for filename in os.listdir(output_directory):
            if filename.startswith(compiled_filename) and filename != compiled_filename:
                os.remove(os.path.join(output_directory, filename))
    
    def __is_package(self, source_file):
        line = source_file.readline()
        source_file.seek(0)
        return not re.match("(.*)(\.css|\.js)", line) is None
    
    def __build_file(self):
        input_file = open(self.input_file_path, "r")
        output_file = open(self.output_file_path, "w+")
        base_directory = os.path.dirname(self.input_file_path)
        file_names = (os.path.basename(self.input_file_path),) if not self.__is_package(input_file) else input_file.readlines() 
        
        for file_name in file_names:
            file_name = file_name.rstrip("\n")
            file_fullpath = os.path.join(base_directory, file_name)
            
            current_file = open(file_fullpath, "r")
            output_file.write("\n\n/* -- %s -- */\n" % file_name)
            
            content = self.__lessify(file_fullpath) if self.apply_less else current_file.read() 
            output_file.write(content)
        
        output_file.close()
    
    
    def __lessify(self, file_path):
        command = u"%s %s" % (settings.LESS_EXECUTABLE, file_path)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, errors = p.communicate()
        
        if out:
            return out
        elif errors:
            logger.error(errors)
            return None
    
    def __get_output_file(self, input_file):
        filename = os.path.split(input_file)[-1]
        hashed_mtime = self.__get_hashed_mtime(self.input_file_path)
        return os.path.join(self.root_path, settings.PACKAGE_DIR, os.path.dirname(input_file), "%s-%s.%s" % (filename, hashed_mtime, self.file_type))
    
    def __get_hashed_mtime(self, filename, length=12):
        try:
            filename = os.path.realpath(filename)
            mtime = str(int(os.path.getmtime(filename)))
        except OSError:
            return None
        return md5_constructor(smart_str(mtime)).hexdigest()[:length]
    
    def __get_file_name(self):
        return "%s%s" % ( settings.STATIC_URL, self.output_file_path[len(self.root_path):].replace(os.sep, '/').lstrip("/"))
    
    
