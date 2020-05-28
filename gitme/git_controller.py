from git import Repo
import git
import logging
import socket


from gitme.command_controller import CommandController


class Git:

    def __init__(self, args):

        self.dir = args.gitrepo
        self.branch = args.branch

        self.commit_message = args.message

        self.repo = Repo(self.dir)
        self.run_command = CommandController.run_command

        self.git_user_attributes = {
            'name': 'gitme',
            'email': 'gitme@' + socket.gethostname()
        }

    def is_modified(self):

        head_commit = self.repo.head.commit
        working_diff = head_commit.diff(None)

        untracked = self.repo.untracked_files

        return any(len(diff) != 0 for diff in [untracked, working_diff])

    def ssh_config_user(self):

        user_attributes = ['name', 'email']

        cmd_base = ['git']
        if self.dir != '':
            cmd_base.append('-C')
            cmd_base.append(self.dir)
        cmd_base.append('config')

        for attr in user_attributes:

            cmd_attr = cmd_base + ['user.' + attr]
            existing_attr = self.run_command(cmd_attr)

            if existing_attr != self.git_user_attributes[attr]:
                cmd_set_attr = cmd_attr + [self.git_user_attributes[attr]]
                self.run_command(cmd_set_attr)

    def create_update_branch(self, heads=None):

        r = self.repo

        if not heads:
            heads = r.remote().fetch()

        remote_head_names = ['/'.join(head.name.split('/')[1:]) for head in heads]
        logging.info('heads: ' + ', '.join(remote_head_names))

        self.ssh_config_user()
        self.change_to_update_branch(remote_head_names)

        modified = self.is_modified()
        diff = []
        if modified:
            diff = self.commit(self.commit_message)
        return modified and len(diff) != 0

    def commit(self, message):
        r = self.repo
        r.git.add('.')
        prev_commit = r.head.commit
        commit = r.index.commit(message)
        logging.info(
            'created commit: {0} {1}'.format(
                commit.hexsha,
                commit.message))
        return prev_commit.diff(commit)

    def change_to_update_branch(self, remote_head_names):

        r = self.repo
        branch = self.branch

        if branch in remote_head_names:

            logging.info('use existing remote branch ' + branch)
            r.git.stash()

            origin = r.remotes['origin']
            origin.fetch()
            r.create_head(branch, origin.refs[branch])\
                .set_tracking_branch(origin.refs[branch])\
                .checkout()

            last_commit = r.head.commit
            if last_commit.message != self.commit_message:
                logging.warning(
                    'abort due to manual modified branch')
                logging.warning(
                    'last commit message: ' + last_commit.message)
                return False

            try:
                r.git.stash('pop')
            except git.GitError as e:
                logging.debug(e)
                logging.debug('reset to master commit to avoid conflicts')
                head_commit = r.heads.master.commit
                r.head.reset(head_commit, index=True, working_tree=True)
                r.git.stash('pop')
        else:
            logging.info('create new branch ' + branch)
            r.create_head(branch).checkout()

        if r.head == branch:
            raise Exception('switch to ref {0} failed'.format(branch))

    def push(self):

        push_args = ['--set-upstream', 'origin', self.branch]

        try:
            self.repo.git.push(push_args)
        except git.GitError:
            logging.info('force pushing because of conflict')
            self.repo.git.push(push_args, force=True)
