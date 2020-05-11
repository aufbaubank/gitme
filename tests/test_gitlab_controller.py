from gitme.entrypoint import create_argparser
from gitme.gitlab_controller import GitlabClient


class TestGitController:

    minimal_args = [
        '-u', 'https://gitlab.localdomain.local',
        '-t', 'invalidtoken'
    ]

    def test_create_instance(self):

        args = create_argparser(TestGitController.minimal_args)
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

        args = create_argparser(TestGitController.minimal_args)
        gl_client = GitlabClient(args)

        for url, name in names:
            extracted = gl_client.extract_gitlab_project_name(url)

            assert isinstance(extracted, str)
            assert extracted != ''
            assert name == extracted
