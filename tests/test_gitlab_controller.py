from gitme.entrypoint import create_argparser
from gitme.gitlab_controller import GitlabClient
import re

class TestGitlabController:

    minimal_args = [
        '-u', 'https://gitlab.localdomain.local',
        '-t', 'invalidtoken'
    ]

    def test_create_instance(self):

        args = create_argparser(TestGitlabController.minimal_args)
        gl_client = GitlabClient(args)

        assert gl_client
        assert gl_client.baseurl == 'https://gitlab.localdomain.local'
        assert gl_client.token == 'invalidtoken'

    def test_extract_projectname(self):

        names = [
            [
                "ssh://gitlab.server.local/group1/project",
                "group1/project"
            ],
            [
                "gitlab.server.local/group1/project",
                "group1/project"
            ],
            [
                "ssh://git@gitlab.server.local/group1/project",
                "group1/project"
            ],
            [
                "git@gitlab.server.local/group1/project",
                "group1/project"
            ],
            [
                "git@gitlab.server.local:2222/group1/project",
                "group1/project"
            ],
            [
                "ssh://git@gitlab.server.local:2222/group1/project",
                "group1/project"
            ],
            [
                "ssh://gitlab.server.local:2222/group1/project",
                "group1/project"
            ],
            [
                "git@github.com:group1/project.git",
                "group1/project"
            ]
        ]

        args = create_argparser(TestGitlabController.minimal_args)
        gl_client = GitlabClient(args)

        for url, name in names:
            extracted = gl_client.extract_gitlab_project_name(url)

            assert isinstance(extracted, str)
            assert extracted != ''
            assert name == extracted

    def test_run_command(self):

        stdout = GitlabClient.run_command(['echo', '123'])

        assert stdout

        output_str = stdout.decode('utf-8')

        assert isinstance(output_str, str)
        assert output_str == '123\n'

    def test_git_remote_url(self):

        url_regex = re.compile('^(https://|git@)github.com[:|/]aufbaubank/gitme.git$')

        args = create_argparser(TestGitlabController.minimal_args)
        gl_client = GitlabClient(args)

        remote_url = gl_client.git_remote_url()

        assert isinstance(remote_url, str)
        assert 'github.com' in remote_url
        assert 'aufbaubank/gitme.git' in remote_url
        assert re.match(url_regex, remote_url)

    def test_project_url(self):

        args = create_argparser(TestGitlabController.minimal_args)
        gl_client = GitlabClient(args)

        project_url = gl_client.project_url()

        assert isinstance(project_url, str)
        assert project_url == 'https://gitlab.localdomain.local/api/v4/projects/aufbaubank%2Fgitme'
