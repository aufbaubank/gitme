import requests
import urllib.parse
import logging
import os
import re

from gitme.command_controller import CommandController


class GitlabClient:

    token_id = 'GITME_TOKEN'

    def __init__(self, args):

        self.branch = args.branch
        self.commit_message = args.message
        self.automerge = args.automerge
        self.git_dir = args.gitrepo

        if args.pat == '' and \
                GitlabClient.token_id in os.environ and \
                os.environ[GitlabClient.token_id] != '':
            self.token = os.environ[GitlabClient.token_id] != ''
        else:
            self.token = args.pat

        self.port_pattern = re.compile(':[0-9]*(/)?')
        self.baseurl = args.url
        self.run_command = CommandController.run_command

    def extract_gitlab_project_name(self, first_line):

        if '://' in first_line:
            stripped_method = first_line.split('://', 1)[1:]
        else:
            stripped_method = [first_line]

        # replace ":22/" with a /, now / is the very first character
        quick_and_dirty = re.sub(self.port_pattern, '/', stripped_method[0])

        stripped_connect = '/'.join(quick_and_dirty.split('/', 1)[1:])
        stripped_git = stripped_connect

        if stripped_git.endswith('.git'):
            stripped_git = stripped_git[:-4]

        return stripped_git

    def git_remote_url(self):

        command = ["git"]
        options = []
        subcommand = [
            'remote',
            '-v',
        ]

        if self.git_dir != '':
            options = options + ['-C', self.git_dir]

        # get the second field from first line
        #
        # git remote -v
        # origin	git@github.com:aufbaubank/gitme.git (fetch)
        # origin	git@github.com:aufbaubank/gitme.git (push)
        #
        stdout = self.run_command(command + options + subcommand)
        origin_fetch_line = ''
        for line in stdout.splitlines():
            if 'origin' in line and '(fetch)' in line:
                origin_fetch_line = line
                break

        if origin_fetch_line == '':
            raise Exception('no git remote found for origin')

        remote_url = origin_fetch_line.split('origin\t')[1].split(' (fetch)')[0]

        return remote_url

    def project_url(self):

        project_name = self.extract_gitlab_project_name(self.git_remote_url())

        url = \
            '{0}/api/v4/projects/{1}'.format(
                self.baseurl,
                urllib.parse.quote(project_name, safe=''))

        return url

    def __req(self, method, endpoint, **kwargs):

        params = {}
        if len(kwargs.keys()) > 0:
            params = kwargs

        # enable to pass protected keywords to kwargs
        prefix = 'python_protected_word_'
        cleaned_params = {}
        for key in params:
            cleaned_params[key.replace(prefix, '')] = params[key]

        headers = {
            "Private-Token": self.token
        }

        url = self.project_url() + endpoint
        response = getattr(requests, method)(
            url,
            params=cleaned_params,
            headers=headers,
            verify=True)

        json = response.json()

        if response.status_code >= 300 or response.status_code < 200:
            if 'error' in json:
                logging.critical('got error from api: {0}'.format(json['error']))
            logging.critical(
                'request {0} failed with status code: {1}'.format(
                    response.url,
                    response.status_code))
            raise Exception('request to gitlab failed')

        return json

    def __get(self, endpoint, **kwargs):
        return self.__req('get', endpoint, **kwargs)

    def __post(self, endpoint, **kwargs):
        return self.__req('post', endpoint, **kwargs)

    def __put(self, endpoint, **kwargs):
        return self.__req('put', endpoint, **kwargs)

    def req_mrs(self):
        # search for merge request
        return self.__get(
            '/merge_requests',
            state='opened',
            source_branch=self.branch,
            target_branch='master',
            with_merge_status_recheck='true',
            search=self.commit_message,
            python_protected_word_in='title'
        )

    def check_permissions(self, project):
        if 'name' in project:
            logging.debug('found project {0}'.format(
                project['name']))
        else:
            raise Exception(
                'project {0} not found or insufficient privileges'.format(
                    self.project_name))

        if not project['merge_requests_enabled']:
            raise Exception('merge requests not enabled!')
        if not project['can_create_merge_request_in']:
            raise Exception('not allowed to create merge requests!')

        pass

    def create_merge_request(self):
        mr = self.__post(
            '/merge_requests',
            source_branch=self.branch,
            target_branch='master',
            title=self.commit_message,
            remove_source_branch=True,
            allow_collaboration=True,
            description=
                '# Autogenerated mergerequest\n'\
                '\n'
                'This Merge request was generated by gitme.\n'\
                '\n'\
                'Automation FTW <3'
        )

        logging.info('created merge request {0}'.format(mr['references']['short']))
        logging.info('url: {0}'.format(mr['web_url']))
        self.recheck_mergerequest(mr)

    def recheck_mergerequest(self, mr):

        if mr['merge_status'] == 'can_be_merged' and \
                not mr['work_in_progress'] and self.automerge:
            res = self.__put(
                '/merge_requests/{0}/merge'.format(mr['iid']),
                should_remove_source_branch=True,
                merge_when_pipeline_succeeds=True,
            )
            if res['merge_when_pipeline_succeeds']:
                logging.info(
                    'automerge for {0} enabled'.format(mr['references']['short']))

        pass

    def create_update_mergerequest(self):

        project = self.__get('')
        self.check_permissions(project)

        mrs = self.req_mrs()

        active_mrs = [mr for mr in mrs if mr['title'] == self.commit_message and mr['state'] == 'opened']

        if len(active_mrs) == 0:
            self.create_merge_request()
        elif len(active_mrs) == 1:
            logging.info('merge request already present: ' + mrs[0]['web_url'])
            self.recheck_mergerequest(mrs[0])

        pass
