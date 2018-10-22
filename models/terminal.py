import shlex
import readline

from models.commands import run_command


class Terminal:
    prompt = "> "

    def run(self):
        while True:
            query = input(self.prompt)

            query = query.strip()

            if not query:
                continue

            argv = shlex.split(query)
            name, *args = argv

            if name == 'exit':
                break

            run_command(name, args)
