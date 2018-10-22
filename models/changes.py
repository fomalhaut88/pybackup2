class BaseChange:
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return "{}(path={})".format(self.__class__.__name__, self.path)


class AddedChange(BaseChange):
    pass


class RemovedChange(BaseChange):
    pass


class UpdatedChange(BaseChange):
    pass
