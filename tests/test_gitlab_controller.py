from gitme.entrypoint import create_argparser
from gitme.gitlab_controller import GitlabClient


class TestGitController:

    def test_create_instance(self):

        args = create_argparser([
            '-u', 'https://gitlab.localdomain.local',
            '-t', 'invalidtoken'
        ])
        gl_client = GitlabClient(args)

        assert gl_client
        assert gl_client.url == 'https://gitlab.localdomain.local/api/v4/projects/gitme'
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
            ]
        ]

        for url, name in names:
            extracted = GitlabClient.extract_giltab_project_name(url)

            assert isinstance(extracted, str)
            assert extracted != ''
            assert name == extracted
