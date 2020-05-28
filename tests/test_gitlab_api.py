from gitme.entrypoint import create_argparser
from gitme.gitlab_controller import GitlabClient
import re
from .responses import mock as Mock


class TestGitlabControllerApi:

    minimal_args = [
        '-u', 'https://localhost',
        '-t', 'invalidtoken'
    ]

    def test_mr_present_checking(self, requests_mock):

        args = create_argparser(TestGitlabControllerApi.minimal_args)
        gl_client = GitlabClient(args)
        mock = Mock.Data(requests_mock)
        mock.mock_mrs_checking()

        gl_client.create_update_mergerequest()

        assert gl_client

    def test_mr_not_present(self, requests_mock):

        args = create_argparser(TestGitlabControllerApi.minimal_args)
        gl_client = GitlabClient(args)
        mock = Mock.Data(requests_mock)
        mock.mock_no_mrs()

        gl_client.create_update_mergerequest()

        assert gl_client
