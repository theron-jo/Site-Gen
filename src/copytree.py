import os, shutil
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
source_dir = os.path.join(project_root, "static")
build_dir = os.path.join(project_root, "docs")

def simple_test():
    print (project_root, source_dir, build_dir)

def validate_source():
    if not os.path.exists(source_dir):
        raise SystemError (False)
    return True

def erase_build_dir():
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    for file_name in os.listdir(build_dir):
        file_path = os.path.join(build_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

def copy_source_to_build():
    if validate_source():
        erase_build_dir()
        shutil.copytree(source_dir, build_dir, dirs_exist_ok=True)


    