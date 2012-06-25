from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor
import logging
import os
import shlex
import subprocess

logger = logging.getLogger("labandas")

class PackageManager(object):
    root_path = settings.STATICFILES_DIRS[0] 
    
    input_file_path = None
    output_file_path = None
    file_type = None
    
    apply_less = False
        
    def load(self, input_path):
        self.file_type = os.path.splitext(input_path)[1].lstrip(".")
        self.input_file_path = os.path.join(self.root_path, input_path)
        self.output_file_path = self.__get_output_file(input_path)
        return self
     
    def build(self):
        self.__build_package()
        
        if self.apply_less and self.file_type == "css":
            self.__build_less()
        
        return self.output_file_path[len(self.root_path):].replace(os.sep, '/').lstrip("/")
    
    def with_less(self):
        self.apply_less = True
        return self
    
    def __build_package(self):
        if os.path.exists(self.output_file_path) and not settings.DEBUG:
            return self
        
        output_directory = os.path.dirname(self.output_file_path)
        
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        input_file = open(self.input_file_path, "r")
        output_file = open(self.output_file_path, "w+")
        base_directory = os.path.dirname(self.input_file_path)
        file_names = input_file.readlines()
        
        for file_name in file_names:
            file_name = file_name.rstrip("\n")
            current_file = open(os.path.join(base_directory, file_name), "r")
            output_file.write("\n\n/* -- %s -- */\n" % file_name)
            output_file.write(current_file.read())
        
        output_file.close()
        
        compiled_filename = os.path.split(self.output_file_path)[-1]
        for filename in os.listdir(output_directory):
            if filename.startswith(compiled_filename) and filename != compiled_filename:
                os.remove(os.path.join(output_directory, filename))
    
    
    def __build_less(self):
        command = u"%s %s" % (settings.LESS_EXECUTABLE, self.output_file_path)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, errors = p.communicate()
        
        if out:
            compiled_file = open(self.output_file_path, "w+")
            compiled_file.write(out)
            compiled_file.close()
            
        elif errors:
            logger.error(errors)
    
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