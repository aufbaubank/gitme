import os


from .git_command import Gitcommand
from gitme.git_controller import Git
from gitme.entrypoint import create_argparser


class TestGitController:

    def test_is_not_modified(self):

        args = create_argparser(['-g', '/tmp/testgit'])

        gc = Gitcommand()
        git = Git(args)

        assert not git.is_modified()

    def test_is_modified_untracked(self):

        args = create_argparser(['-g', '/tmp/testgit'])

        gc = Gitcommand()
        git = Git(args)

        gc.create_untracked()
        assert git.is_modified()

    def test_is_modified_tracked(self):
        args = create_argparser(['-g', '/tmp/testgit'])

        gc = Gitcommand()
        git = Git(args)

        gc.create_untracked()
        gc.track_all()
        assert git.is_modified()

#    def test_create_update_branch_new(self):
#        args = create_argparser(['-g', '/tmp/testgit'])
#
#        gc = Gitcommand()
#        git = Git(args)
#
#        gc.create_untracked()
#        gc.track_all()
#
#        git.create_update_branch()
#
#    def test_create_update_branch_existing(self):
#        args = create_argparser(['-g', '/tmp/testgit'])
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
#        with open('/tmp/testgit/existingbranch', 'w') as f:
#            f.write('initial content\n\n')
#
#        git.create_update_branch()
#        gc.switch_branch('master')
#
#        with open('/tmp/testgit/existingbranch', 'w+') as f:
#            f.write('additional content\n\n')
#
#        git.create_update_branch()
#        gc.switch_branch('master')
#
#        assert not os.path.exists('/tmp/testgit/existingbranch')
#        gc.switch_branch('gitme/update')
#        with open('/tmp/testgit/existingbranch', 'r') as f:
#            content = f.read()
#            assert content == 'additional content\n\n'
#
#    def test_create_update_branch_existing_same_content(self):
#        args = create_argparser(['-g', '/tmp/testgit'])
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
#        with open('/tmp/testgit/existingbranch', 'w') as f:
#            f.write('initial content\n\n')
#
#        git.create_update_branch()
#        gc.switch_branch('master')
#
#        with open('/tmp/testgit/existingbranch', 'w+') as f:
#            f.write('additional content\n\n')
#
#        git.create_update_branch()
#        gc.switch_branch('master')
#
#        assert not os.path.exists('/tmp/testgit/existingbranch')
#        gc.switch_branch('gitme/update')
#        with open('/tmp/testgit/existingbranch', 'r') as f:
#            content = f.read()
#            assert content == 'additional content\n\n'
#        assert gc.count_commits() == 2
#
#
#        # do additional modify, same content as before
#        gc.switch_branch('master')
#        with open('/tmp/testgit/existingbranch', 'w+') as f:
#            f.write('additional content\n\n')
#        git.create_update_branch()
#        gc.switch_branch('master')
#        assert not os.path.exists('/tmp/testgit/existingbranch')
#        gc.switch_branch('gitme/update')
#        with open('/tmp/testgit/existingbranch', 'r') as f:
#            content = f.read()
#            assert content == 'additional content\n\n'
#
#        assert gc.count_commits() == 2
