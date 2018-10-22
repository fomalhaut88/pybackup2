from models.errors import CommandError


class BaseCommand:
    command = None
    args = ()
    doc = ""

    def __init__(self, *args):
        if len(args) != len(self.__class__.args):
            raise CommandError("invalid number of arguments")

        self.args = {
            key: arg
            for key, arg in zip(self.__class__.args, args)
        }

    def execute(self):
        raise NotImplementedError()
