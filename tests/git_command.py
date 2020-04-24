import os
import shutil
import subprocess


class Gitcommand:

    def __init__(self, working_dir='/tmp/testgit'):

        self.dir = working_dir
        self.__remove_gitdir()
        os.mkdir(self.dir)

        for i in ['file1', 'file2']:
            with open(self.dir + '/' + i, 'w') as f:
                f.write('initial content\n\n')

        self.cmd_base = 'git -C ' + self.dir + ' '

        sequence = [
            self.cmd_base + 'init --quiet',
            self.cmd_base + 'add .',
            self.cmd_base + 'config user.email "you@example.com"',
            self.cmd_base + 'config user.name "Your Name"',
            self.cmd_base + 'commit -m "initial commit" --quiet'
        ]

        for cmd in sequence:
            os.system(cmd)

    def __del__(self):
        self.__remove_gitdir()
        pass

    def __remove_gitdir(self):
        if os.path.isfile(self.dir):
            os.remove(self.dir)
        elif os.path.isdir(self.dir):
            shutil.rmtree(self.dir)

    def create_untracked(self):
        for i in ['ut1', 'ut2']:
            with open(self.dir + '/' + i, 'w') as f:
                f.write('initial content\n\n')

    def track_all(self):
        os.system(self.cmd_base + 'add .')

    def commit(self):
        os.system(self.cmd_base + 'commit -m "my commit" --quiet')

    def create_switch_branch(self, branch):
        os.system(self.cmd_base + 'checkout -b ' + branch + ' --quiet')

    def switch_branch(self, branch='master'):
        os.system(self.cmd_base + 'checkout ' + branch + ' --quiet')

    def count_commits(self):
        base = self.cmd_base.split(' ')[:-1]
        arguments = base + ['log', '--pretty=oneline']
        ret = subprocess.run(arguments, stdout=subprocess.PIPE)
        return len(ret.stdout.splitlines())
