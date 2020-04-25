import gitme
import re


class TestRunCommand:

    def test_no_arguments(self, script_runner):

        ret = script_runner.run('gitme')

        assert ret
        assert ret.success
        assert ret.stderr == ''
        assert ret.stdout != ''

    def test_version(self, script_runner):

        version_regex = re.compile('[0-9]\\.[0-9]?.[0-9]?\\n')
        version = gitme.__version__
        ret = script_runner.run('gitme', '--version')

        assert ret
        assert ret.success
        assert ret.stderr == ''
        assert ret.stdout == '{0}\n'.format(version)
        assert version_regex.match(ret.stdout)
