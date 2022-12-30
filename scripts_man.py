import pathlib
import os
import datetime
import shutil
import sys
import time
from rich.status import Status


# [author]:         Donald Guiles
# [script]:         scripts_man.py
# [date]:           December 29 2022
#
# [description]:
#     
#   Look through various user directories and collect copies of all the scripts 
#   into the Scripts directory in home. 




##############################
# Classes
##############################

class Directory:
    home = pathlib.Path().home()
    scripts = f"{home}/Scripts"
    python = f"{scripts}/python"
    go = f"{scripts}/go"
    cpp = f'{scripts}/cpp'
    sh = f'{scripts}/sh'
    js = f'{scripts}/js'
    html = f'{scripts}/html'
    desktop = f"{home}/Desktop"
    downloads = f'{home}/Downloads'
    clang = f"{scripts}/clang"
    headers = f"/home/{os.getlogin()}/Scripts/clang/headers"
    o = f"home/{os.getlogin()}/Scripts/clang/o"



##############################
# Declare
##############################

directories = [
    Directory.scripts, Directory.python, Directory.go, 
    Directory.cpp, Directory.sh, Directory.js, 
    Directory.html, Directory.desktop, Directory.downloads, 
    Directory.clang, Directory.headers, Directory.o
    ]

script_directories = {
    'py':Directory.python, 'go':Directory.go, 
    'cpp':Directory.cpp, 'sh':Directory.sh, 
    'js':Directory.js, 'html':Directory.html,
    'o':Directory.o, 'h':Directory.headers, 
    'c':Directory.clang
}

extensions = [f".{x}" for x in script_directories.keys()]
dont_search = [Directory.scripts, Directory.js, Directory.clang, Directory.go, Directory.python, Directory.headers, Directory.o, Directory.html]
subdirs = []

##############################
# Functions
##############################

def delete_all():
    os.sync()
    for directory in script_directories.values()[1:-2]:
        message('deleting', directory)
        shutil.rmtree(directory)
        os.sync()


def check_os():
    """ Check the operating system and declare if usable 
    """

    osl = sys.platform[0].lower()
    if osl in ['l', 'd']:
        pass
    else:
        print("windows is not supported yet")
        exit()

def file_exists_in_scripts(filename: str):
    """ checks to see if a filename/filepath already exists in scripts home 
    """

    extension = filename.split(".")[1]
    try:
        path = script_directories[extension]
    
        files = [x for x in os.listdir(path)]
        if filename in files:
            return True
        else:
            return False
    except:
        return True

def copy_file_to_script_home(filepath: str):
    """ try to copy a file to the scripts home 
        
        :filepath: the full path to the original file 
    """

    filename = filepath.split("/")[-1]
    extension = filename.split(".")[-1]
    script_home = script_directories[extension]
    destination = f"{script_home}/{filename}"    
    if not file_exists_in_scripts(filename):
        try:
            shutil.copy(src=filepath, dst=destination)
        except PermissionError:
            message('error', f'Permission Not Granted  -> {filename}')
        except shutil.RegistryError:
                message('error', f'Permission Not Granted  -> {filename}')
        except shutil.SameFileError:
            message('error', f'Same File Exists -> {filename}')
        except FileNotFoundError:
            message('not found', filepath)

def message(title, message):
    """ print a colored update message 
    """
    
    print(f"[\033[2m{datetime.datetime.utcnow()}\033[0m][\033[32m{title}\033[0m]: \033[3m{message}\033[0m")

def make_directories():
    """ check and make the neccessary directories 
    """
    os.sync()
    for directory in directories:
        try:
            os.mkdir(directory)
            message('created', directory)
        except FileExistsError:
            continue
        except FileNotFoundError:
            continue

def get_files(directory: str):
    """ get fullpaths for the given directory 
    """

    match directory:
        case 'desktop':
            return [f"{Directory.desktop}/{x}" for x in os.listdir(Directory.desktop) if pathlib.Path(x).is_file()]
        case 'home':
            return [f"{Directory.home}/{x}" for x in os.listdir(Directory.home) if pathlib.Path(x).is_file()]
        case 'downloads':
            return [f"{Directory.downloads}/{x}" for x in os.listdir(Directory.downloads) if pathlib.Path(x).is_file()]        

def check_extensions(filepath: str):
    """ check to see if the file has one of the collecting extensions 
    """
    
    for ext in extensions:
            if filepath.endswith(ext):
                return True
    return False

def scan_home():
    """ check home directory for scripts to add to the collection 
    """
    
    files = get_files('home')
    for file in files:
        myfile = file
        if check_extensions(myfile):
            copy_file_to_script_home(myfile)

def scan_desktop():
    """ check desktop directory for scripts to add to the collection 
    """

    files = get_files('desktop')
    for file in files:
        myfile = file
        if check_extensions(myfile):
            copy_file_to_script_home(myfile)

def scan_downloads():
    """ check the downloads directory for scripts to add to the collection 
    """

    files = get_files('downloads')
    for file in files:
        myfile = file
        if check_extensions(myfile):
            copy_file_to_script_home(myfile)


def print_timer():
    """ util for recording the speed of the operations 
    """
    
    t1 = time.time()
    print(t1)
    return t1

def delta_time(time1, time2):
    """ calculate the change in time from one time to another, 
        used for measuring the speed 
    """

    dt = time2 - time1
    message(' Total Time ', f'{dt} in seconds')
    return dt


def file_search(directory: str):
    """ get all the files on the drive """

    message("collecting", 'all files')
    for root, dirs, files in os.walk(directory):
        message('scanning', root)
        if root in dont_search:
            message('Found', root)
            continue
        for file in files:
            if check_extensions(file):
                filepath = f'{root}/{file}'
                message('checking', filepath)
                copy_file_to_script_home(filepath)

def search_user():
    """ search the user space """

    message('searching', os.getlogin())
    file_search(Directory.home)

def search_from_root():
    """ search from the root of the drive """

    message('searching', 'entire drive')
    file_search("/")

def main_root():
    """ main function but instead searches all the directories 
    """
    with Status("Scanning from root...", spinner='aesthetic') as status:
        t1 = print_timer()
        make_directories()
        check_os()
        search_from_root()
        t2 = print_timer()
        delta_time(t1, t2)


def main():
    """ Scan downloads, desktop and home directory
        for scripts for go, cpp, python, js, html etc 
    """

    t1 = print_timer()
    precheck()
    message('searching', 'Home Directory')
    scan_home()
    message('searching', 'Desktop Directory')
    scan_desktop()
    message('searching', 'Downloads Directory')
    scan_downloads()
    t2 = print_timer()
    delta_time(t1, t2)

def precheck():
    """ check files and dependencies 
    """

    message('precheck', 'Checking Files')
    check_os()
    make_directories()



if __name__ == '__main__':
    main_root()
