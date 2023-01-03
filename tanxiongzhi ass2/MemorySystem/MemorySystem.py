from __future__ import annotations

import os
from typing import Any

DIR_MAX_ELEMS = 5
SEPARATOR = '/'
MAX_BUF_FILE_SIZE = 10

class MemorySystem():

    def change_working_directory(self, path):
        dest = self.get_tree_node(path)
        
        if not isinstance(dest, Directory):
            raise ValueError("Destination is not a directory")

        self.cwd = dest

    def __init__(self):
        self.base_root = Directory(self, path=[], name="~")
        self.cwd = self.base_root


    def path_to_string(self, path: list[TreeNode]) -> str:
        return SEPARATOR.join(path)

    def get_tree_node(self, path) -> TreeNode:
        return self.cwd.get_node_2(path)

    def create_directory(self, path: str, name: str) -> Directory:
        dest_dir = self.get_tree_node(path)
        os.mkdir(path + '/' + name)

    def create_binary_file(self, path: str, name: str, info: str) -> BinaryFile:
        dest_dir = self.get_tree_node(path)
        return dest_dir.create_binary_file(name, info)

    def create_log_file(self, path: str, name: str, info: str = None) -> LogFile:
        dest_dir = self.get_tree_node(path)
        return dest_dir.create_log_file(name, info)

    def create_buffer(self, path: str, name: str) -> BufferFile:
        dest_dir = self.get_tree_node(path)
        return dest_dir.create_buffer(name)

    def print_elements(self) -> None:
        print(self.cwd.name)
        self.cwd.print_elements(lvl=0)

    def delete_file(self, name):
        try:
            os.rmdir(name)
            print("Successfully delete such directory")
        except:
            print("Fail to delete")


class TreeNode:
    # it shows that path of the node and name of node
    def __init__(self, path: list[TreeNode], name: str):
        self.path = path
        self.name = name

    def delete(self):
        farther = self.path[-1]
        farther.childs.pop(farther.son.index(self))

    
class Directory(TreeNode):
    def __init__(self, fs: MemorySystem, path: list[TreeNode], name: str):
        if SEPARATOR in name:
            print("you have already contains this")

        self.son = []
        self.fs = fs
        super().__init__(path, name)

    # it shows the move from source to destination
    def move_dir(self, filename: str, destination: str):
        dest_directory = self.fs.get_tree_node(destination)

        ans = None

        try:
            for s in self.son:
                if s.name == filename:
                    ans = s
        except:
            print("file not exist or wrong path")


        self.son.remove(ans)
        dest_directory.son.append(ans)


    def create_directory(self, name: str) -> Directory:
        if len(self.son) == DIR_MAX_ELEMS:
            print("can't create")

        for child in self.son:
            if child.name == name:
                print('file already exist')

        self.son.append(Directory(self.fs, self.path + [self], name))

    def create_binary_file(self, name: str, information: str) -> BinaryFile:
        if len(self.son) == DIR_MAX_ELEMS:
            print("can't create")

        for child in self.son:
            if child.name == name:
                print('file already exist')
        file = BinaryFile(self.path + [self], name, information)
        self.son.append(file)

        return file


    def create_log_file(self, name: str, info: str = None) -> LogFile:
        if len(self.son) == DIR_MAX_ELEMS:
            print("can't create")

        for child in self.son:
            if child.name == name:
                print('file already exist')
        file = LogFile(self.path + [self], name, info)
        self.son.append(file)

        return file

    def create_buffer(self, name: str) -> BufferFile:
        if len(self.son) == DIR_MAX_ELEMS:
            print("can't create")

        for child in self.son:
            if child.name == name:
                print('file already exist')
        file = BufferFile(self.path + [self], name)
        self.son.append(file)

        return file

    def print_elements(self, lvl=0) -> None:
        for child in self.son:
            print("  "*(lvl+1) + child.name)
            
            if isinstance(child, Directory):
                child.print_elements(lvl+1)

    def get_node_2(self, path):
        dest_dir_name = path.split(SEPARATOR)[0]
        ans = None

        try:
            if dest_dir_name == '.':
                ans = self
            elif dest_dir_name == '..':
                ans = self.path[-1]
            elif dest_dir_name == '~':
                ans = self.fs.base_root
        except:
            print("error")

        for s in self.son:
            if s.name == dest_dir_name:
                ans = s

        if SEPARATOR in path:
            return ans.get_node_2(SEPARATOR.join(path.split(SEPARATOR)[1:]))
        else:
            return ans


class BinaryFile(TreeNode):
    def __init__(self, path: list[TreeNode], name: str, info: str):
        if SEPARATOR in name:
            print("error")
            return
        super().__init__(path, name)
        self.info = info

    def read(self) -> None:
        return self.info


class BufferFile(TreeNode):
    def __init__(self, path: list[TreeNode], name: str):
        if SEPARATOR in name:
            print("error")

        super().__init__(path, name)
        self.items = []

    def push(self, element: Any) -> bool:
        if len(self.items) >= MAX_BUF_FILE_SIZE:
            print("error")
            return
        self.items.append(element)

    def pop(self) -> bool:
        if len(self.items) == 0:
            print("error")
            return
        return self.items.pop()

class LogFile(TreeNode):
    def __init__(self, path: list[TreeNode], name: str, info: str = ""):
            
        super().__init__(path, name)
        self.info = info

    def read(self) -> str:
        return self.info

    def append(self, info: str) -> str:
        self.info += info


