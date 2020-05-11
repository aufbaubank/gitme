import requests
import urllib.parse
import subprocess
import logging
import os


class GitlabClient:

    token_id = 'GITME_TOKEN'

    def __init__(self, args):

        self.branch = args.branch
        self.commit_message = 'update files'
        self.automerge = args.automerge
        self.git_dir = args.gitrepo

        if args.pat == '' and \
                GitlabClient.token_id in os.environ and \
                os.environ[GitlabClient.token_id] != '':
            self.token = os.environ[GitlabClient.token_id] != ''
        else:
            self.token = args.pat

        git_remote_url = subprocess.run(
            [
                'git',
                '-C',
                self.git_dir,
                'remote',
                'get-url',
                'origin'
            ],
            stdout=subprocess.PIPE
        ).stdout.splitlines()[0].decode('utf-8')

        self.project_name = self.extract_giltab_project_name(git_remote_url)
        self.url = \
            '{0}/api/v4/projects/{1}'.format(
                args.url,
                urllib.parse.quote(self.project_name, safe=''))

    @staticmethod
    def extract_giltab_project_name(first_line):

        if '://' in first_line:
            stripped_method = first_line.split('://', 1)[1:]
        else:
            stripped_method = [first_line]

        stripped_connect = '/'.join(stripped_method[0].split('/', 1)[1:])
        stripped_git = stripped_connect

        if stripped_git.endswith('.git'):
            stripped_git = stripped_git[:-4]

        return stripped_git

    def __req(self, method, endpoint, **kwargs):

        params = {}
        if len(kwargs.keys()) > 0:
            params = kwargs

        headers = {
            "Private-Token": self.token
        }

        url = self.url + endpoint
        response = getattr(requests, method)(
            url,
            params=params,
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
            source_branch=self.branch,
            target_branch='master'
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
            title='update files',
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

        active_mrs = [mr for mr in mrs if mr['title'] == 'update files' and mr['state'] == 'opened']

        if len(active_mrs) == 0:
            self.create_merge_request()
        elif len(active_mrs) == 1:
            logging.info('merge request already present: ' + mrs[0]['web_url'])
            self.recheck_mergerequest(mrs[0])

        pass
