import re
import socket

from .git_command import Gitcommand
from gitme.git_controller import Git
from gitme.entrypoint import create_argparser
from gitme.command_controller import CommandController


class TestGitController:

    def test_is_not_modified(self):

        args = create_argparser(['-g', '/tmp/gitme'])

        gc = Gitcommand()
        git = Git(args)

        assert not git.is_modified()

    def test_is_modified_untracked(self):

        args = create_argparser(['-g', '/tmp/gitme'])

        gc = Gitcommand()
        git = Git(args)

        gc.create_untracked()
        assert git.is_modified()

    def test_is_modified_tracked(self):
        args = create_argparser(['-g', '/tmp/gitme'])

        gc = Gitcommand()
        git = Git(args)

        gc.create_untracked()
        gc.track_all()
        assert git.is_modified()

    def test_create_update_branch_new(self):
        args = create_argparser(['-g', '/tmp/gitme'])

        gc = Gitcommand()
        git = Git(args)

        gc.create_untracked()
        gc.track_all()

        assert git.create_update_branch()

    def test_create_update_branch_new_and_untracked(self):
        args = create_argparser(['-g', '/tmp/gitme'])

        gc = Gitcommand()
        git = Git(args)

        gc.create_untracked()

        assert git.create_update_branch()

    def test_ssh_config_user(self):
        args = create_argparser(['-g', '/tmp/gitme'])

        gc = Gitcommand()
        git = Git(args)

        git.ssh_config_user()

        assert 'gitme\n' == gc.get_user_name()
        assert 'gitme@' + socket.gethostname() + '\n' == gc.get_user_email()
        assert re.match(r'gitme@[a-zA-Z0-9.-]+\n', gc.get_user_email())

    # def test_create_update_branch_existing(self):
    #
    #     class Head:
    #
    #         def __init__(self, name):
    #
    #             self.name = name
    #
    #     heads = [Head('origin/gitme/update')]
    #
    #     args = create_argparser(['-g', '/tmp/gitme'])
    #
    #     gc = Gitcommand()
    #     git = Git(args)
    #
    #     gc.create_switch_branch('gitme/update')
    #     gc.create_untracked()
    #     gc.track_all()
    #     gc.commit()
    #     gc.switch_branch('master')
    #
    #     with open('/tmp/gitme/existingbranch', 'w') as f:
    #         f.write('initial content\n\n')
    #
    #     git.create_update_branch(heads)
    #     gc.switch_branch('master')
    #
    #     with open('/tmp/gitme/existingbranch', 'w+') as f:
    #         f.write('additional content\n\n')
    #
    #     git.create_update_branch()
    #     gc.switch_branch('master')
    #
    #     assert not os.path.exists('/tmp/gitme/existingbranch')
    #     gc.switch_branch('gitme/update')
    #     with open('/tmp/gitme/existingbranch', 'r') as f:
    #         content = f.read()
    #         assert content == 'additional content\n\n'
    #
#    def test_create_update_branch_existing_same_content(self):
#        args = create_argparser(['-g', '/tmp/gitme'])
#
#        gc = Gitcommand()
#        git = Git(args)
#
#        gc.create_switch_branch('gitme/update')
#        gc.create_untracked()
#        gc.track_all()
#        gc.commit()
#        gc.switch_branch('master')
#
#        with open('/tmp/gitme/existingbranch', 'w') as f:
#            f.write('initial content\n\n')
#
#        git.create_update_branch()
#        gc.switch_branch('master')
#
#        with open('/tmp/gitme/existingbranch', 'w+') as f:
#            f.write('additional content\n\n')
#
#        git.create_update_branch()
#        gc.switch_branch('master')
#
#        assert not os.path.exists('/tmp/gitme/existingbranch')
#        gc.switch_branch('gitme/update')
#        with open('/tmp/gitme/existingbranch', 'r') as f:
#            content = f.read()
#            assert content == 'additional content\n\n'
#        assert gc.count_commits() == 2
#
#
#        # do additional modify, same content as before
#        gc.switch_branch('master')
#        with open('/tmp/gitme/existingbranch', 'w+') as f:
#            f.write('additional content\n\n')
#        git.create_update_branch()
#        gc.switch_branch('master')
#        assert not os.path.exists('/tmp/gitme/existingbranch')
#        gc.switch_branch('gitme/update')
#        with open('/tmp/gitme/existingbranch', 'r') as f:
#            content = f.read()
#            assert content == 'additional content\n\n'
#
#        assert gc.count_commits() == 2
