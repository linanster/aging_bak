import os, shutil

from app.settings import logfolder, appfolder



def empty_dir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        # print('==root==', root)
        for name in files:
            # print('==file==', name)
            if name =='.gitkeep':
                continue
            os.remove(os.path.join(root, name))
        for name in dirs:
            # print('==dir==', name)
            # os.removedirs(os.path.join(root, name))
            os.rmdir(os.path.join(root, name))

def rm_pycache(path):
     for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            if name == '__pycache__':
                # os.removedirs(os.path.join(root, name))
                shutil.rmtree(os.path.join(root, name))


def cleanup_log():
    empty_dir(logfolder)

def cleanup_pycache():
    rm_pycache(appfolder)
