import os
import shutil

class Clean:
    def __init__(self):
        pass
    def remove(self, session):
        rootDir = './files'
        for dirpath, dirnames, filenames in os.walk(rootDir, topdown=False):
            for dirname in dirnames:
                if dirname == str(session):
                    dirToRemove = os.path.join(dirpath, dirname)
                    shutil.rmtree(dirToRemove)