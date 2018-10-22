from models.base_command import BaseCommand
from models import __version__


class Version(BaseCommand):
    title = 'version'
    args = ()
    doc = "Prints version of Pybackup."

    def execute(self):
        print(__version__)
