import os
import json
import glob


class Data:

    def __init__(self, requests_mock):

        self.location = os.path.dirname(os.path.realpath(__file__))
        self.requests_mock = requests_mock

    def get_response_filepaths(self):

        return glob.glob(self.location + '/*.json')

    def mock_json_responses_from_files(self, files):

        defaults = {
            'status_code': 200,
            'method': 'get'
        }

        """ load data """
        for file in files:
            with open(self.location + '/' + file, 'r') as file:

                res = json.load(file)

                for key in defaults.keys():
                    if key not in res:
                        res[key] = defaults[key]

                self.requests_mock.register_uri(
                    res['method'],
                    res['url'],
                    json=res['body'],
                    status_code=res['status_code']
                )

    def mock_mrs_checking(self):

        files = [
            "get_projects.json",
            "get_mrs_checking.json"
        ]

        self.mock_json_responses_from_files(files)

        pass

    def mock_no_mrs(self):

        self.mock_json_responses_from_files([
            "get_projects.json",
            "get_mrs_empty.json",
            "post_mr.json"
        ])

