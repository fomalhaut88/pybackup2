import os


__version__ = 'dev'


CONFIG_PATH = os.path.join(
    os.path.expanduser("~"),
    ".pybackup"
)


if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)
