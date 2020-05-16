import os
import shutil
import subprocess


class Gitcommand:

    def __init__(self, working_dir='/tmp/gitme'):

        self.dir = working_dir
        self.__remove_gitdir()
        os.system('git -C /tmp clone https://github.com/aufbaubank/gitme')

        self.cmd_base = 'git -C ' + self.dir + ' '

    def __del__(self):
        self.__remove_gitdir()
        pass

    def __remove_gitdir(self):
        if os.path.isfile(self.dir):
            os.remove(self.dir)
        elif os.path.isdir(self.dir):
            shutil.rmtree(self.dir)

    def construct_command(self, additional_params):

        if isinstance(additional_params, str):
            ary = additional_params.split(' ')
        elif isinstance(additional_params, bytearray):
            ary = additional_params
        else:
            raise Exception('parameter not allowed : ' + additional_params)

        base = self.cmd_base.split(' ')[:-1]
        cmd = base + ary

        return cmd

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
        cmd = self.construct_command('log --pretty=oneline')
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        return len(ret.stdout.splitlines())

    def get_user_name(self):
        cmd = self.construct_command('config user.name')
        decoded_stdout = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        return decoded_stdout

    def get_user_email(self):
        cmd = self.construct_command('config user.email')
        decoded_stdout = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        return decoded_stdout

