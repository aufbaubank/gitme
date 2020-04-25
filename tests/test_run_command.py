import gitme


class TestRunCommand:

    def test_no_arguments(self, script_runner):

        ret = script_runner.run('gitme')

        assert ret
        assert ret.success
        assert ret.stderr == ''
        assert ret.stdout != ''

    def test_version(self, script_runner):

        version = gitme.__version__
        ret = script_runner.run('gitme', '--version')

        assert ret
        assert ret.success
        assert ret.stderr == ''
        assert ret.stdout == '{0}\n'.format(version)
