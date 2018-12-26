import os
import sys


CONFIG_PATH = os.path.abspath(".pybackup2")
BASE_DIR = sys._MEIPASS if getattr(sys, 'frozen', False) else '.'


with open(os.path.join(BASE_DIR, 'version')) as f:
    __version__ = f.read().strip()


if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)
