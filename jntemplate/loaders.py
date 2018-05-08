# -*- coding: utf-8 -*-
from abc import abstractclassmethod, ABCMeta
import os

__all__ = ["BaseLoader", "FileLoader"]


class BaseLoader(metaclass=ABCMeta):

    @abstractclassmethod
    def load(self, name, encoding, *directory):
        pass

    @abstractclassmethod
    def get_directory(self, path):
        pass


class FileLoader(BaseLoader):
    def __init__(self):
        self.directories = []

    def load(self, name, encoding, *directory): 
        if not os.path.isabs(name):
            i, full = self.find(
                list(directory) + self.directories + [os.getcwd()], name)
            if(i == -1):
                return None, None
            return self.read(full, encoding), full
        return self.read(name, encoding), name

    def get_directory(self, path):
        return os.path.dirname(path)

    def parse_path(self, res_file):
        # print("sss..ss".index('..'))
        # print(type("sss..ss"))
        # print(str(res_file).index('..'))
        if res_file == None or res_file.startswith(".."):
            return None
        return res_file.replace("/", os.sep)

    def find(self, paths, name):
        if name == None:
            return -1, None
        name = self.parse_path(name)
        if name == None:
            return -1, None
        for i in range(len(paths)):
            if paths[i][-1] == os.sep:
                full = paths[i]  + name
            else:
                full = paths[i] + os.sep+ name
            print (full)
            if os.path.exists(full) and os.path.isfile(full):
                return i, full
        return -1, None

    def read(self, path, encoding):
        with open(path, "r", encoding=encoding) as f:
            return f.read()
