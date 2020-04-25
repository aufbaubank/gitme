# gitme

[![Build Status](https://travis-ci.com/aufbaubank/gitme.svg?branch=master)](https://travis-ci.com/aufbaubank/gitme)
[![codecov](https://codecov.io/gh/aufbaubank/gitme/branch/master/graph/badge.svg)](https://codecov.io/gh/aufbaubank/gitme)
![PyPI](https://img.shields.io/pypi/v/gitme)
![PyPI - Downloads](https://img.shields.io/pypi/dm/gitme)
![PyPI - License](https://img.shields.io/pypi/l/gitme)
![PyPI - Format](https://img.shields.io/pypi/format/gitme)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/gitme)

Can be used to create a merge request on gitlab for a changed repostory.

Desired Workflow:
1. periodically run some tasks in a git repository that may change some files
2. run `gitme`
3. a merge request is created, if files have changed

## Features

* creates branch
* creates merge request
* automerge
* updates existing branch, that is not merged yet

## options

```
usage: gitme [-h] [-u url] [-t pat] [-a] [-g gitrepo] [-b branch] [-V]
             [-l LOGLEVEL] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -u url, --url url     url of gitlab server, defaults to http://localhost
  -t pat, --pat pat     personal access token
  -a, --automerge       automerge merge requests if pipeline succeeds
  -g gitrepo, --gitrepo gitrepo
                        repository location
  -b branch, --branch branch
                        branch name, default: gitme/update
  -V, --version         print version
  -l LOGLEVEL, --loglevel LOGLEVEL
                        loglevel: critical, error, warning, info, debug
  -v, --verbose
```
