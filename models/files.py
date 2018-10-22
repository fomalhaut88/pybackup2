import sys
import os

from models.utils import unordered_lists_equal


class BaseFile:
    def __init__(self, name):
        self.name = name

    def print(self, stream=sys.stdout, offset=0):
        raise NotImplementedError()

    def as_dict(self):
        raise NotImplementedError()

    def equal(self, obj, with_content=True):
        raise NotImplementedError()

    def generate_to(self, base):
        raise NotImplementedError()

    @classmethod
    def create_from(cls, base, with_content=True):
        raise NotImplementedError()


class File(BaseFile):
    def __init__(self, name, content=''):
        super().__init__(name)
        self.content = content

    def print(self, stream=sys.stdout, offset=0):
        print(' ' * offset + '* ' + self.name, file=stream)

    def as_dict(self):
        return {
            'type': 'file',
            'name': self.name
        }

    def equal(self, obj, with_content=True):
        if isinstance(obj, self.__class__):
            return self.name == obj.name and (not with_content or self.content == obj.content)
        else:
            return False

    def generate_to(self, base):
        path = os.path.join(base, self.name)
        with open(path, 'w') as f:
            f.write(self.content)

    @classmethod
    def create_from(cls, base, with_content=True):
        name = os.path.basename(base)
        if with_content:
            with open(base) as f:
                content = f.read()
        else:
            content = ''
        return cls(name=name, content=content)


class Dir(BaseFile):
    def __init__(self, name, dirs=None, files=None):
        super().__init__(name)
        self.dirs = dirs if dirs is not None else []
        self.files = files if files is not None else []

    def print(self, stream=sys.stdout, offset=0):
        print(' ' * offset + '- ' + self.name, file=stream)
        for d in self.dirs:
            d.print(stream, offset + 3)
        for f in self.files:
            f.print(stream, offset + 3)

    def as_dict(self):
        return {
            'type': 'dir',
            'name': self.name,
            'dirs': list(map(Dir.as_dict, self.dirs)),
            'files': list(map(File.as_dict, self.files))
        }

    def equal(self, obj, with_content=True):
        return (
            isinstance(obj, self.__class__) and
            obj.name == self.name and
            unordered_lists_equal(obj.dirs, self.dirs, cmp_func=lambda a, b: a.equal(b, with_content=with_content)) and
            unordered_lists_equal(obj.files, self.files, cmp_func=lambda a, b: a.equal(b, with_content=with_content))
        )

    def generate_to(self, base):
        path = os.path.join(base, self.name)
        os.mkdir(path)
        for d in self.dirs:
            d.generate_to(path)
        for f in self.files:
            f.generate_to(path)

    @classmethod
    def create_from(cls, base, with_content=True):
        name = os.path.basename(base)
        dirs = []
        files = []
        for n in os.listdir(base):
            path = os.path.join(base, n)
            if os.path.isdir(path):
                d = Dir.create_from(path, with_content=with_content)
                dirs.append(d)
            else:
                f = File.create_from(path, with_content=with_content)
                files.append(f)
        return cls(name=name, dirs=dirs, files=files)
