import config
import os

VERSION_PATH = os.path.join(config.dirpath, 'src', 'VERSION')


with open(VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()
